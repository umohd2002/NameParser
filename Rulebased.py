import re
from DB_Operations import DB_Operations

class RuleBasedNameParser:
    def NameParser(line, key, values):

        MASK=[] #In String
        #print(line)
        USAD_Conversion_Dict = {"USNM_GSF": "", "USNM_STL": "", "USNM_PTL": "", "USNM_GNM": "", "USNM_SNM": "", "USNM_NA": ""}
        List=USAD_Conversion_Dict.keys()
        FirstPhaseList=[]
        ck = key
        cv = values
        NameList=line
        TrackKey=[]
        Mask=[]
        Combine=""
        Compare=False
        LoopCheck=1
        # last_comma_index = None
        # for A in NameList:
        #     print(A)
        #     FirstPhaseDict={}
        #     NResult=False
        #     try:
        #         Compare=A[0].isdigit()
        #     except:
        #         print()
        last_comma_index = None
        # if NameList.count(',') >>1:
        #     NameList = [name for name in NameList if name != ',']
        c=0    #print(NameList)
        commaCount = 0
        for idx, A in enumerate(NameList):
            FirstPhaseDict = {}
            NResult = False
            if A == ",":
                #print(NameList)
                O = 0
                Combine = ","
                Mask.append(Combine)
                TrackKey.append(",")
                FirstPhaseDict[","] = A
                FirstPhaseList.append(FirstPhaseDict)
                last_comma_index = idx
                commaCount+=1
            elif A == " ":
                continue
            elif A != "," and len(A) == 1:
                Combine += "I"
                TrackKey.append("I")
                FirstPhaseDict["I"] = A
                FirstPhaseList.append(FirstPhaseDict)
            else:
                for k in range(len(ck)):
                    if A ==ck[k]:
                        temp=cv[k]
                        NResult=True
                        Combine+=temp
                        FirstPhaseDict[temp] = A 
                        FirstPhaseList.append(FirstPhaseDict)
                        TrackKey.append(temp)
                if NResult==False:
                    Combine+="W"
                    TrackKey.append("W")
                    FirstPhaseDict["W"] = A
                    FirstPhaseList.append(FirstPhaseDict)
            if LoopCheck==len(NameList):
                Mask.append(Combine)
            
            LoopCheck+=1
        
        USAD_Mapping = {"USNM_GSF": [], "USNM_STL": [], "USNM_PTL": [], "USNM_SNM": [], "USNM_GNM": [], "USNM_NA": []}
        Start = 0
        Counts = 0

        Final_Map = [None] * len(FirstPhaseList)
        last_w_index = None
        # print(f"TrackKey: {TrackKey}, Combine: {Combine}, temp: {temp}")
        for idx, key in enumerate(TrackKey):
            if key == "W" or key =='I':
                last_w_index = idx
                #print(f"last_w_index: {last_w_index}, key: {key}, TrackKey: {TrackKey}")

        #print("FirstPhaseList:", FirstPhaseList)
        # print("Input Line:", line)
        #print(f"last_w_index: {last_w_index}")
        for R in USAD_Conversion_Dict:
            for j in range(len(TrackKey)):
                Dictionary = FirstPhaseList[j]
                
                
                
                # print("Processing Dictionary:", Dictionary)
                Key = ""
                Value = ""
                for K, V in Dictionary.items():
                    Key = K
                    Value = V
                if R == "USNM_GSF" and Key == "G":
                    USAD_Mapping["USNM_GSF"].append(j + 1)
                    USAD_Conversion_Dict["USNM_GSF"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_GSF", Key]
                    
                elif R == "USNM_PTL" and Key == "P":
                    USAD_Mapping["USNM_PTL"].append(j + 1)
                    USAD_Conversion_Dict["USNM_PTL"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_PTL", Key]
                    
                elif R == "USNM_GNM" and (Key == "W" or Key == "I") and j != last_w_index:
                    #print(f"TrackKey[j+1]: {TrackKey[j+1]}")
                    if j+1 < len(TrackKey) and j+1 < len(NameList) and TrackKey[j+1] != ',' and TrackKey[j+1] != ' ' :
                        USAD_Mapping["USNM_GNM"].append(j + 1)
                        USAD_Conversion_Dict["USNM_GNM"] += " " + Value.strip()
                        Final_Map[j] = [Value.strip(), "USNM_GNM", Key]
                    elif c==0:
                        USAD_Mapping["USNM_SNM"].append(j + 1)
                        USAD_Conversion_Dict["USNM_SNM"] += " " + Value.strip()
                        Final_Map[j] = [Value.strip(), "USNM_SNM", Key]
                        c=c+1
                    
                    else:
                        USAD_Mapping["USNM_GNM"].append(j + 1)
                        USAD_Conversion_Dict["USNM_GNM"] += " " + Value.strip()
                        Final_Map[j] = [Value.strip(), "USNM_GNM", Key]

                elif R == "USNM_STL" and Key == "Q":
                    USAD_Mapping["USNM_STL"].append(j + 1)
                    USAD_Conversion_Dict["USNM_STL"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_STL", Key]
                    
                elif R == "USNM_GNM" and (Key == "I" or Key == "W"):
                    USAD_Mapping["USNM_GNM"].append(j + 1)
                    USAD_Conversion_Dict["USNM_GNM"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_GNM", Key]
                    
                elif R == "USNM_SNM" and Key == "L":
                    USAD_Mapping["USNM_SNM"].append(j + 1)
                    USAD_Conversion_Dict["USNM_SNM"] += " " + Value.strip()
                    Final_Map[j] = [Value.strip(), "USNM_SNM", Key]
                    
        if last_w_index is not None:
            next_index=None
            next_w_index=None
           # print("Processing Dictionary:", Dictionary)
            #print("last_comma_index Dictionary:", last_comma_index)
            Dictionary = FirstPhaseList[last_w_index]
            if last_w_index + 1 < len(FirstPhaseList):
                W_next = FirstPhaseList[last_w_index + 1]
                for p, q in W_next.items():
                    next_w_index = p
             #       print('wnext', next_w_index)
            if last_comma_index is not None and not last_comma_index+1:
                Dict_next = FirstPhaseList[last_comma_index+1]
                for r, s in Dict_next.items():
                    next_index = r
                 #   print('next',next_index)
                  #  print('next_dict', Dict_next)
                
            
            Key = ""
            Value = ""
            
            for K, V in Dictionary.items():
                Key = K
                Value = V
            #print('c',c)
            if last_comma_index is not None  and c>=1 and (next_w_index!='W' and next_w_index!='I'):
                USAD_Mapping["USNM_GNM"].append(last_w_index + 1)
                USAD_Conversion_Dict["USNM_GNM"] += " " + Value.strip()
                Final_Map[last_w_index] = [Value.strip(), "USNM_GNM", Key]
            else:
                USAD_Mapping["USNM_SNM"].append(last_w_index + 1)
                USAD_Conversion_Dict["USNM_SNM"] += " " + Value.strip()
                Final_Map[last_w_index] = [Value.strip(), "USNM_SNM", Key]
               # print('xxxx')
        
            

        #print("Final_Map before cleanup:", Final_Map)
        
        # Remove None entries
        Final_Map = [entry for entry in Final_Map if entry is not None]
        
        # Adjust Final_Map to exclude comma if necessary
# =============================================================================
#         if ',' in line:
#             comma_index = None
#             for idx, token in enumerate(NameList):
#                 if token == ',':
#                     comma_index = idx
#                     break
#             if comma_index is not None and comma_index < len(Final_Map):
#                 del Final_Map[comma_index]
# =============================================================================
        
        #print("Final_Map after cleanup:", Final_Map)
        return Final_Map

# Example usage:

