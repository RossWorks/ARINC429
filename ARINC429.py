class Frame:

    _SSM_Table=("Failure Warning",
                "Functional Test",
                "Not Computed Data",
                "Normal Operation")

    _LogicalFrame : dict = {}
    _BinaryWord   : str

    def _CheckIntegrity(self,
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
               ICD = None,
               Channel : str = "") -> Exception:
        Label  : str
        Fields : list
        self._LogicalFrame.clear()
        FirstCheck = self._CheckIntegrity(Frame)
        if FirstCheck != 0:
            self._LogicalFrame = {}
            return Exception(FirstCheck)
        Tmpstr=Frame[24:32]
        Label = oct(int(Tmpstr[::-1],2))
        self._LogicalFrame["LABEL"]=Label
        SSM = Frame[1:3]
        self._LogicalFrame["SSM"]=self._SSM_Table[int(SSM,2)]
        SDI = Frame[22:24]
        self._LogicalFrame["SDI"]=SDI
        PAYLOAD=Frame[3:22]
        self._LogicalFrame["PAYLOAD"]=PAYLOAD
        if (ICD == None):
            return Exception(0)
        if not ICD.Valid:
            return Exception(0)
        if Channel not in ICD._ChannelList:
            return Exception(6)
        Key = Channel + ';' + Label[2::]
        if not ICD.FindKey(Key):
            return Exception(7)
        Fields = ICD._Content[Key]
        if Fields[0].SDI[0:2] == 'XX':
            self._AttachSDI()
        FieldDict = self._ParsePayload(Fields)
        self._LogicalFrame.update(FieldDict)
        return Exception(0)

    def GetLogicalData(self) -> dict:
        return self._LogicalFrame

    def _AttachSDI(self):
        self._LogicalFrame["PAYLOAD"] += self._LogicalFrame["SDI"]
        self._LogicalFrame["SDI"] = "Extended label"

    def _ParsePayload(self,
                      DataFields : list) -> dict:
        FieldDict = dict()
        for field in DataFields:
            if field.Name[0:4] == "SSM_":
                continue
            if field.Encoding == "BNR":
                FieldDict[field.Name] = self._DecodeBNR(MSB = field.MSB,
                                                      LSB = field.LSB)
        return FieldDict

    def _DecodeBNR(self,
                   MSB,
                   LSB) -> str:
        strPayload  = self._LogicalFrame["PAYLOAD"]
        RightBound  = 32 - int(MSB) - 3
        LeftBound   = 32 - int(LSB) - 3 + 1
        SignBitVal  = -int(strPayload[0]) * pow(2, (len(strPayload) - 1))
        OtherBits   = int(strPayload[RightBound+1:LeftBound],base = 2)
        LogicalData = SignBitVal + OtherBits
        return str(LogicalData)

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

    _ChannelList = []
    _Content     = {}
    Valid  : bool = False

    def __init__(self) -> None:
        pass

    def GetChannelList(self) -> list:
        return self._ChannelList 

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
            if Channel not in self._ChannelList:
                self._ChannelList.append(Channel)
            TmpField = self.DataField(Name     = TmpLine[0],
                                      Encoding = TmpLine[3],
                                      MSB      = TmpLine[4],
                                      LSB      = TmpLine[5],
                                      SDI      = TmpLine[6])
            if Key not in self._Content:
                self._Content[Key] = list()
            self._Content[Key].append(TmpField)
        ICDfile.close()
        self.Valid = True
        return Exception(0)

    def FindKey(self,
                Key = "") -> bool:
        if Key in self._Content:
            return True
        else:
            return False
    
    def ExtractKey(self,
                   Key : str) -> list:
        return self._Content[Key]

    def Invalidate(self):
        self.Valid = False

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