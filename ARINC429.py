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
    class DataField:
        Name     : str
        Encoding : str
        MSB      : int
        LSB      : int
        SDI      : str

        def __init__(self,
                     Name,
                     Encoding,
                     MSB,
                     LSB,
                     SDI) -> None:
            self.Name     = Name
            self.Encoding = Encoding
            self.MSB      = MSB
            self.LSB      = LSB
            self.SDI      = SDI

    __ChannelList = []
    __Data        = {}

    def __init__(self) -> None:
        pass

    def GetChannelList(self) -> list:
        return self.__ChannelList 

    def Load(self,
             FileDir : str) -> Exception:
        TmpLine = [str]
        try:
            ICDfile=open(FileDir)
        except:
            return Exception(4)
        for line in ICDfile:
            if line[0] == '#':
                continue
            TmpLine=str.split(line,sep=';')
            if len(TmpLine) <= 1:
                return Exception(5)
            Channel = TmpLine[1]
            Label   = TmpLine[2]
            Key     = Channel + ';' + Label
            if Channel not in self.__ChannelList:
                self.__ChannelList.append(Channel)
            TmpField = self.DataField(Name     = TmpLine[0],
                                      Encoding = TmpLine[3],
                                      MSB      = TmpLine[4],
                                      LSB      = TmpLine[5],
                                      SDI      = TmpLine[6])
            if Key not in self.__Data:
                self.__Data[Key] = list()
            self.__Data[Key].append(TmpField)
        ICDfile.close()
        return Exception(0)

class Exception:
    title   : str
    message : str
    Code    : int

    def __init__(self,Code : int = 0) -> None:
        self.Code = Code
        if Code == 0:
            self.title   = "No errors"
            self.message = "Execution exited normally"
        elif Code == 1:
            self.title   = "ARINC Frame"
            self.message = "ARINC Frame is not 32 bits long"
        elif Code == 2:
            self.title   = "ARINC Frame"
            self.message = "ARINC Frame is not binary"
        elif Code == 3:
            self.title   = "ARINC Frame"
            self.message = "ARINC Frame must have odd parity"
        elif Code == 4:
            self.title   = "ICD file"
            self.message = "Unable to open ICD file"
        elif Code == 5:
            self.title   = "ICD file"
            self.message = "Invalid ICD file"
        else:
            self.title   = "Unknown exception"
            self.message = "Unknown exception"
        self.message += "\nError code: " + str(Code)

if __name__ == "__main__":
    print("ARINC429 library by RossWorks.")
    print("Please refer to documentation to learn how to use this library")