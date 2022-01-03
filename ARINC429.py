class Frame:

    __SSM_Table=("Failure Warning",
                 "Functional Test",
                 "Not Computed Data",
                 "Normal Operation")

    __LogicalFrame={}
    __BinaryWord : str

    def __CheckIntegrity(self,
                       Frame) -> int:
        oneCount : int = 0
        if len(Frame) != 32:
            return 1
        for bit in Frame:
            if (bit != '0' and bit != '1'):
                return 2
            if (bit == '1'):
                oneCount +=1 
        if oneCount % 2 == 0:
            return 3
        return 0

    def Decode(self,
               Frame) -> Exception:
        Label : str
        FirstCheck = self.__CheckIntegrity(Frame)
        if FirstCheck != 0:
            self.__LogicalFrame.clear()
            return Exception(FirstCheck)
        Label = oct(int(Frame[-8:-1],2))
        self.__LogicalFrame["LABEL"]=Label
        SSM = Frame[1:3]
        self.__LogicalFrame["SSM"]=self.__SSM_Table[int(SSM,2)]
        SDI = Frame[-11:-9]
        self.__LogicalFrame["SDI"]=SDI
        PAYLOAD=Frame[3:-11]
        self.__LogicalFrame["PAYLOAD"]=PAYLOAD
        return Exception(0)

    def GetLogicalData(self) -> dict:
        return self.__LogicalFrame

class ICD:
    pass

class Exception:
    title   : str
    message : str
    Code    : int

    def __init__(self,Code : int = 0) -> None:
        self.Code = Code
        if Code == 0:
            self.title   = "No errors"
            self.message = "Execution exited normally\nException code: " + str(Code)
        elif Code == 1:
            self.title   = "ARINC Frame"
            self.message = "ARINC Frame is not 32 bits long\nException code: " + str(Code)
        elif Code == 2:
            self.title   = "ARINC Frame"
            self.message = "ARINC Frame is not binary\nException code: " + str(Code)
        elif Code == 3:
            self.title   = "ARINC Frame"
            self.message = "ARINC Frame must have odd parity\nException code: " + str(Code)
        else:
            self.title   = "Unknown exception"
            self.message = "Unknown exception code is " + str(Code)

if __name__ == "__main__":
    print("ARINC429 library by RossWorks.")
    print("Please refer to documentation to lern how to use this library")