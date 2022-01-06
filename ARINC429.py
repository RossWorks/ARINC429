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
               Frame,
               ICD,
               Channel = "") -> Exception:
        Label  : str
        Fields : list
        FirstCheck = self.__CheckIntegrity(Frame)
        if FirstCheck != 0:
            self.__LogicalFrame.clear()
            return Exception(FirstCheck)
        Tmpstr=Frame[24:32]
        Label = oct(int(Tmpstr[::-1],2))
        self.__LogicalFrame["LABEL"]=Label
        SSM = Frame[1:3]
        self.__LogicalFrame["SSM"]=self.__SSM_Table[int(SSM,2)]
        SDI = Frame[22:24]
        self.__LogicalFrame["SDI"]=SDI
        PAYLOAD=Frame[3:22]
        self.__LogicalFrame["PAYLOAD"]=PAYLOAD
        if not ICD.Valid:
            return Exception(0)
        if Channel == "":
            return Exception(6)
        Key = Channel + ';' + Label[2::]
        if not ICD.FindKey(Key):
            return Exception(7)
        Fields = ICD.__Content[Key]
        print("ICD extracted")
        return Exception(0)

    def GetLogicalData(self) -> dict:
        return self.__LogicalFrame

    def __AttachSDI(self) -> str:
        pass

    def __ParsePayload(self) -> dict:
        pass

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
    __Content     = {}
    Valid  : bool = False

    def __init__(self) -> None:
        pass

    def GetChannelList(self) -> list:
        return self.__ChannelList 

    def Load(self,
             FileDir : str) -> Exception:
        TmpLine = [str]
        self.Valid   = False
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
            if Key not in self.__Content:
                self.Content[Key] = list()
            self.Content[Key].append(TmpField)
        ICDfile.close()
        self.Valid = True
        return Exception(0)

    def FindKey(self,
                Key = "") -> bool:
        if Key in self.Content:
            return True
        else:
            return False

class Exception:
    title   : str
    message : str
    Code    : int

    def __init__(self,Code : int = 0) -> None:
        self.Code = Code
        if   Code == 0:
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
        elif Code == 6:
            self.title   = "ARINC Channel"
            self.message = "Provided invalid ARINC Channel"
        elif Code == 7:
            self.title   = "ARINC label"
            self.message = "ARINC label not found in ICD"
        else:
            self.title   = "Unknown exception"
            self.message = "Unknown exception"
        if   Code != 0:
            self.message += "\nError code: " + str(Code)

if __name__ == "__main__":
    print("ARINC429 library by RossWorks.")
    print("Please refer to documentation to learn how to use this library")