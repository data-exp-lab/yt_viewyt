import yt


class YtObject(object):
    r"""A basic representation of a data object loaded through yt.

    This is the object that is used to track all objects that have been
    loaded with yt or created by a method written in yt, like novel data
    objects.

    Notes
    ------
    This is a weak class at the moment, and could utilize a lot of work.
    Some improvements that could be made:
    -Support for icons that distinguish what frontend yt is using, and if the
    object is a single data object or a data series.
    -Methods to create novel data objects from the initial file loaded, and to
    name those novel objects
    -Methods to save data objects"""

    def __init__(self):
        super(YtObject, self).__init__()

    def get_name(self):
        r"""Returns the name of the object instance"""
        pass

    def get_data(self):
        r"""Returns a reference to the actual data handled by yt."""
        pass

    def get_data_type(self):
        r"""Returns the type of the object in yt."""
        pass


class YtFrontEndObject(YtObject):
    r"""A basic representation of any data object created by being
    loaded through yt.

    Parameters
    -----------
    file_name : string or list of string
        The name of the file or files from which the instance is being
        initialized.
    """

    def __init__(self, file_name):
        super(YtFrontEndObject, self).__init__()

        if isinstance(file_name, list):
            self.data = yt.load(file_name)
            self.data_type = "data set series"
            self.name = "Needs Work"
        else:
            self.data = yt.load(file_name)
            self.data_type = str(type(self.data))
            self.data_type = self.data_type.split('.')[-1]
            self.data_type = self.data_type.strip(">")
            self.data_type = self.data_type.strip("'")
            self.name = file_name

    def get_name(self):
        r"""Return the name of the Yt Object.

        Returns
        -------
        string
            The name of the instance of object."""
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
        r"""Returns the type of the object.

        Returns
        -------
        string
            The type of the object."""
        return self.data_type


class YtDataObject(YtObject):
    r"""A representation of all objects created in yt by specifying selection
    parameters for a region from data loaded into yt.

    Parameters
    ----------
    yt_object : YtDataContainer
        The object which this object holds and references.
    name : string
        The name of this instance of data."""

    def __init__(self, yt_object, name):
        self.data = yt_object
        self.name = name
        self.data_type = str(type(self.data))
        self.data_type = self.data_type.split('.')
        self.data_type = self.data_type[-1]
        self.data_type = self.data_type.strip(">")
        self.data_type = self.data_type.strip("'")

    def get_name(self):
        r"""Return the name of the Yt Object.

        Returns
        -------
        string
            The name of the instance of object."""

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
        r"""Returns the type of the object.

        Returns
        -------
        string
            The type of the object."""
        return self.data_type
