from abc import ABC, abstractmethod

class BaseFormatTransform(ABC):
    """
    Base class for format transformation.
    """

    @abstractmethod
    def transform(self, data:  str)-> str:
        """
        Transform the data.
        """
        pass

    @abstractmethod
    def validate(self, data: str)->bool:
        """
        Validate the input data is supportive or not.
        """
        pass

    def apply_transform(self, data: str)-> str:
        """
        Apply the transformation to the data.
        """
        if self.validate(data):
            try:
                output = self.transform(data)
                return output
            except Exception as e:
                raise ValueError("Error occurred during transformation: " + str(e))
        else:
            raise ValueError("Invalid input data")