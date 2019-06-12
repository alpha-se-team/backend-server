# DatabaseStorage for django.
# 2009 (c) GameKeeper Gambling Ltd, Ivanov E.

from django.core.files.storage import Storage
from django.core.files import File
from django.conf import settings

import StringIO
import urlparse

import pyodbc


class DatabaseStorage(Storage):
    """Class DatabaseStorage provides storing files in the database.

    Class DatabaseStorage can be used with either FileField or ImageField.
It can be used to map filenames to database blobs: so you have to use it
with a special additional table created manually. The table should contain a
pk-column for filenames
(better to use the same type that FileField uses: nvarchar(100)), blob field
(image type for example) and size field (bigint).
You can't just create blob column in the same table, where you defined
FileField, since there is no way to find required row in the save() method.
    Also size field is required to obtain better perfomance (see size()
method).
    So you can use it with different FileFields and even with different
"upload_to" variables used. Thus it implements a kind of root filesystem,
where you can define dirs using "upload_to" with FileField and store any
files in these dirs.
    It uses either settings.DB_FILES_URL or constructor param 'base_url'
(@see __init__()) to create urls to files. Base url should be mapped to view
that provides access to files. To store files in the same table, where
FileField is defined you have to define your own field and provide extra
argument (e.g. pk) to save().

    Raw sql is used for all operations. In constractor or in DB_FILES of
settings.py () you should specify a dictionary with db_table, fname_column,
blob_column,
    size_column and 'base_url'. For example I just put to the settings.py
the following line:
      DB_FILES = {'db_table': 'FILES', 'fname_column':  'FILE_NAME',
'blob_column': 'BLOB', 'size_column': 'SIZE', 'base_url': 'http://localhos
/dbfiles/' }"
    And use it with ImageField as following:
      player_photo = models.ImageField(upload_to="player_photos", storage =
DatabaseStorage() )

    DatabaseStorage class uses your settings.py file to perform custom
connection to your database.
    The reason to use custom connection:
http://code.djangoproject.com/ticket/5135
    Connection string looks like
"cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=testdb
UID=me;PWD=pass')"

    It's based on pyodbc module, so can be used with any database supported
by pyodbc.
    I've tested it with MS Sql Express 2005.

    @note It returns special path, which should be mapped to special view,
which returns requested file:
      @code
      def image_view(request, filename):
          import os
          from django.http import HttpResponse
          from django.conf import settings
          from django.utils._os import safe_join
          from filestorage import DatabaseStorage
          from django.core.exceptions import ObjectDoesNotExist

          storage = DatabaseStorage()

          try:
              image_file = storage.open(filename, 'rb')
              file_content = image_file.read()
          except:
              filename = 'no_image.gif'
              path = safe_join(os.path.abspath(settings.MEDIA_ROOT), filename)
              if not os.path.exists(path):
                  raise ObjectDoesNotExist
              no_image = open(path, 'rb')
              file_content = no_image.read()

          response = HttpResponse(file_content, mimetype="image/jpeg")
          response['Content-Disposition'] = 'inline; filename=%s'%filename
          return response
      @endcode

    @note If filename exist, blob will be overwritten, to change this remove
get_available_name(self, name), so Storage.get_available_name(self, name)
will be used to
    generate new filename.
    """

    def __init__(self, option=settings.DB_FILES):
        """Constructor.

        Constructs object using dictionary either specified in contucotr or
in settings.DB_FILES.

        @param option dictionary with 'db_table', 'fname_column',
'blob_column', 'size_column', 'base_url'  keys.

        option['db_table']
            Table to work with.
        option['fname_column']
            Column in the 'db_table' containing filenames (filenames can
contain pathes). Values should be the same as where FileField keeps
filenames.
            It is used to map filename to blob_column. In sql it's simply
used in where clause.
        option['blob_column']
            Blob column (for example 'image' type), created manually in the
'db_table', used to store image.
        option['size_column']
            Column to store file size. Used for optimization of size()
method (another way is to open file and get size)
        option['base_url']
            Url prefix used with filenames. Should be mapped to the view,
that returns an image as result.
        """

        if not option or not (option.has_key('db_table')
                              and option.has_key('fname_column')
                              and option.has_key('blob_column')
                              and option.has_key('size_column')
                              and option.has_key('base_url')):
            raise ValueError("You didn't specify required options")
        self.db_table = option['db_table']
        self.fname_column = option['fname_column']
        self.blob_column = option['blob_column']
        self.size_column = option['size_column']
        self.base_url = option['base_url']

        #get database settings
        self.DATABASE_ODBC_DRIVER = settings.DATABASE_ODBC_DRIVER
        self.DATABASE_NAME = settings.DATABASE_NAME
        self.DATABASE_USER = settings.DATABASE_USER
        self.DATABASE_PASSWORD = settings.DATABASE_PASSWORD
        self.DATABASE_HOST = settings.DATABASE_HOST

        self.connection = pyodbc.connect(
            'DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' %
            (self.DATABASE_ODBC_DRIVER, self.DATABASE_HOST, self.DATABASE_NAME,
             self.DATABASE_USER, self.DATABASE_PASSWORD))
        self.cursor = self.connection.cursor()

    def _open(self, name, mode='rb'):
        """Open a file from database.

        @param name filename or relative path to file based on base_url. path should contain only "/", but not "\". Apache sends pathes with "/".
        If there is no such file in the db, returs None
        """

        assert mode == 'rb', "You've tried to open binary file without specifying binary mode! You specified: %s" % mode

        row = self.cursor.execute("SELECT %s from %s where %s = '%s'" %
                                  (self.blob_column, self.db_table,
                                   self.fname_column, name)).fetchone()
        if row is None:
            return None
        inMemFile = StringIO.StringIO(row[0])
        inMemFile.name = name
        inMemFile.mode = mode

        retFile = File(inMemFile)
        return retFile

    def _save(self, name, content):
        """Save 'content' as file named 'name'.

        @note '\' in path will be converted to '/'.
        """

        name = name.replace('\\', '/')
        binary = pyodbc.Binary(content.read())
        size = len(binary)

        #todo: check result and do something (exception?) if failed.
        if self.exists(name):
            self.cursor.execute(
                "UPDATE %s SET %s = ?, %s = ? WHERE %s = '%s'" %
                (self.db_table, self.blob_column, self.size_column,
                 self.fname_column, name), (binary, size))
        else:
            self.cursor.execute(
                "INSERT INTO %s VALUES(?, ?, ?)" % (self.db_table),
                (name, binary, size))
        self.connection.commit()
        return name

    def exists(self, name):
        row = self.cursor.execute("SELECT %s from %s where %s = '%s'" %
                                  (self.fname_column, self.db_table,
                                   self.fname_column, name)).fetchone()
        return row is not None

    def get_available_name(self, name):
        return name

    def delete(self, name):
        if self.exists(name):
            self.cursor.execute("DELETE FROM %s WHERE %s = '%s'" %
                                (self.db_table, self.fname_column, name))
            self.connection.commit()

    def url(self, name):
        if self.base_url is None:

            raise ValueError("This file is not accessible via a URL.")
        return urlparse.urljoin(self.base_url, name).replace('\\', '/')

    def size(self, name):
        row = self.cursor.execute("SELECT %s from %s where %s = '%s'" %
                                  (self.size_column, self.db_table,
                                   self.fname_column, name)).fetchone()
        if row is None:
            return 0
        else:
            return int(row[0])
