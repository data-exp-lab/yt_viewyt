import yt


class YtObject(object):
    def __init__(self):
        super(YtObject, self).__init__()

    def get_name(self):
        pass

    def get_data(self):
        pass

    def get_data_type(self):
        pass


class YtFrontEndObject(YtObject):
    r"""A basic representation of a data object loaded through yt.

    This is the object that is used to track all objects that have been
    loaded with yt or created by a method written in yt, like novel
    data objects.

    Parameters
    -----------
    data : yt.frontends object
        The actual data object referenced by yt.

    dataType : string
        This parameter references whether the data loaded into yt is a dataset
        series or a single data object. It will ultimately be used to determine
        whether widgets that manipulate the time step of a view will be
        available or not.

    name : string
        The name of the loaded object. It defaults to the name of the filename
        in the case of a single data object.

    Notes
    ------
    This is a weak class at the moment, and could utilize a lot of work.
    Some improvements that could be made:
    -Support for icons that distinguish what frontend yt is using, and if the
    object is a single data object or a data series.
    -Methods to create novel data objects from the initial file loaded, and to
    name those novel objects
    -Methods to save data objects
    """

    def __init__(self, fileName):
        r"""Initializes an instance of the YtObject.

        Specifically, this creates an instance of YtObject based on the type
        of `fileName`. If it is a list, the initialization assumes a
        data series.

        Parameters
        ----------
        fileName : string or list of string
            The name of the file from which the instance is being
            initialized.

        Returns
        -------
        self : YtObject"""
        super(YtFrontEndObject, self).__init__()

        if isinstance(fileName, list):
            self.data = yt.load(fileName)
            self.data_type = "data set series"
            self.name = "Needs Work"
        else:
            self.data = yt.load(fileName)
            self.data_type = str(type(self.data))
            self.data_type = self.data_type.split('.')[-1]
            self.data_type = self.data_type.strip(">")
            self.data_type = self.data_type.strip("'")
            self.name = fileName

    def get_name(self):
        return self.name

    def get_data(self):
        r"""Returns the yt data object for the given instance

        Returns
        -------
        data : yt.frontend_like
            The data from the instance of the YtObject.
        """
        return self.data

    def get_data_type(self):
        return self.data_type


class YtDataObject(YtObject):

    def __init__(self, yt_object, name):
        self.data = yt_object
        self.name = name
        self.data_type = str(type(self.data))
        self.data_type = self.data_type.split('.')
        self.data_type = self.data_type[-1]
        self.data_type = self.data_type.strip(">")
        self.data_type = self.data_type.strip("'")

    def get_name(self):
        return self.name

    def get_data(self):
        return self.data

    def get_data_type(self):
        return self.data_type
