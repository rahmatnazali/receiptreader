import re

fullstring_1 = "BC LIQUORSTORES\nCELEBRATE LIFE .ENJOYRESPONSIBLY\n*********************************\nk******\n#123 Kingsgate Mall BCLS\n#122-370 E Broadway\nVancouver , BC V5T 4G5\nPhone: (604) 660-6675\nFax: (604) 872-6895\n****\nCustomer #: 305810\nCust PST #: P10093339\nFOX\n*******\nName:\nAddress:\n2321 MAIN STREET\nVANCOUVER\nBC\nV5T 3C9\n1438\nCAPTAIN MORGAN WHITE 1X1.14L\n66.98 G\n2 @ 33.49\nContainer Deposit\n773143\nCAZADORES BLANCO 1X750ml\n0.40\n159.95 G\n5 @ 31.99\nContainer Deposit\n0.50\n226.93\nSubtotal\n0.90\n11.35\nContainer Deposit Subtotal\nG GST 5%\n239.18\nTotal\nBC Liquor Store # 123\nAug 10 2019 03:37 pmTrans# 301587057583\nTRANSACTION RECORD\nCard:************4112\nA0000000031010\nVISA CREDIT\nTrans Type\nCard Entry\nAuth #\nSequence #\nMerchant ID\nTerminal #\nDate\nTime\nCard Type: VI\nPURCHASE\n: C\n:024275\n: 001001185\n:22109801\nB42210980101\n:08-10-2019\n15:37:47\n$239.18\nAmount\n00 APPROVED THANK YOU\nRetain this copy for your\nrecords\n*** CUSTOMER COPY ***\nTotal Count of Items\n7\nGST Reg #124542945\nX 1 012 3 0 15870575 8 3\nThanks for shopping BC Liquor Stores\nTransaction Number 1012301587057583\nStr\n10/08/2019\nReg\n3:37 PM\n01\n123\n*********\n******\nBCLDB Return Policy: Refunds accepted\nwithin 60 days with receipt. Refund\npolicy detail available online at\nwww.bcliquorstores.com\n"
fullstring_2 = "BC LIQUORSTORES\nCELEBRATE LIFE..ENJ\n* * YRESPONSIBLY\nk************\n#123 Kingsgate Mall BCLS\n#122 370 E Broadway\nVancouver , BC V5T 4G5\nPhone:(604) 660-6675\nFax: (604) 872-6895\n************\n********\nCustomer #: 305810\nCust PST #: P10093339\nFOX\nName:\nAddress:\n2321 MAIN STREET\nVANCOUVER\n\u0412\u0421\nBC\nV5T 3C9\n***\n************\n928374\nJAMESON IRISH 1X1.14L\n145.47 G\n3 48.49\nContainer Deposit\n1453\nTANQUERAY LONDON DRY 1X1.14L\n0.60\n101.97 G\n3 @ 33.99\n35.99\nRegularly\nContainer Deposit\n471\nSEAGRAM'S V O 1X1.14L\n0.60\n67.98 G\n2 @ 33.99\nContainer Deposit\n773143\nCAZADORES - BLANCO 1X750ml\n0.40\n127.96 G\n4 31.99\nContainer Deposit\n1438\nCAPTAIN MORGAN WHITE 1X1.14L\n0.40\n66.98 G\n2 @ 33.49\nContainer Deposit\n19557\nLAMARCA PROSECCO 1X187ml\n0.40\n44.34 G\n6 @ 7.39\n7.99\nRegularly\nContainer Deposit\n0.60\nSubtotal\n554.70\nContainer Deposit Subtotal\nG GST 5%\n3.00\n27.74\nTotal\n585.44\nBC Liquor Store # 123\nAug 03 2019 02:46 pmTrans# 301586985795\nTRANSACTION RECORD\nCard:************4112\nA0000000031010\nVISA CREDIT\nTrans Type\nCard Entry\nAuth #\nSequence #\nMerchant ID\nTerminal #\nDate\nTime\nCard Type: VI\nPURCHASE\nC\n:080567\n:001001087\n22109801\nB42210980101\n:08-03-2019\n14:46:0\n:$585.44\nAmount\nTHANK YOU\n00 APPROVED\nRetain this copy for your\nrecords\n*** CUSTOMER COPY ***\n20\nTotal Count of Items\nGST Reg #124542945\nYou saved:\n$9.60\nX 101230 1 5 86 9 85795\n"
fullstring_3 = "BC LIQUORSTORES\nCELEBRATE LIFE...ENJOYRESPONSIBLY\n*** ***************************\n#111 Commercial Drive BCLS\n1520 Commercial Drive\nVancouver, BC V5L 3Y2\nPhone:604-660-9088\nFax: 604-660-9732\n**\nCustomer #: 176878\nCust PST #:\nName:\nAddress:\nk*******\nk****\nP11024702\nFAYUCA\n1009 HAMILTON ST\nVANCOUVER\nBC\nV682R9\n***\n*******\n**********\n6502\nCOINTREAU 1X750ml\n203.94 G.\n6 @ 33.99\nContainer Deposit\n856914\nSOMBRA MEZCAL 1X750ml\n0.60\n635.88 G\n12 52.99\n54.99\nRegularly\nContainer Deposit\n773143\nCAZADORES BLANCO 1X750ml\n1.20\n359.88 G\n12 @ 29.99\n31.99\nRegularly\nContainer Deposit\n242669\nGONZALEZ BYASS TIO PEPE 1X750ml\n1.20\n47.98 G\n2 @ 23.99\nContainer Deposit\n641068\nSIPS CATALUNYA BLANCA ALTA 1x750ml\n0.20\n245.88 G\n1220,49\nContainer Deposit\n1.20\nSubtotal\n1,493.56\nContainer Deposit Subtotal\nG- GST 5%\n4.40\n74.68\nTotal\n1,572.64\nBC Liquor Store\n111\nMay 24 2019 01:39 pm Trans# 114586277525\nTRANSACTION RECORD\nCard:************6433\nCard Type\nTrans Type\nCard Entry\nAuth #\nSequence #\nMerchant ID\nTerminal #\nDate\nTime\n: MC\n:MOTO PURCHASE\nM\n:08655S\n:001001495\n:22109256\n: B42210925614\n:05-24-2019\n:13:39:55\nAmount\n$1572.64\nAPPROVED\nTHANK YOU\n"
fullstring_4 = "BC LIQUORSTORES\nCELEBRATE LIFE...ENJOYRESPONSIBLY\n**** *******************************\nBCLS #160 39th & Cambie\n5555 Cambie Street\nVancouver, BC V5Z 3A3\nPhone: 604-660-9463\nFax: 604-664-0878\n*** ***********************************\nCustomer #: 304872\nCust PST : P10014990\nName:\nAddress:\nNUBA ON BROADWAY\n3116 BROADHAY WEST\nVANCOUVER\nBC\nV6K 2G9\n*************************\n*****\n*\n197.88 G\n357327\nROAD13 HONEST JOHN'S ROSE 1X750m\n1216.49\n1.20\n59.98 G\nContainer Deposit\n460378\nEL JIMADOR BLANCO 1X750mL\n2 @ 29.99\n31.99\nRegularly\nContainer Deposit\n178012\nTRIPLE SEC HENKES 1X750ml\n0.20\n83.96 G\n4 20.99\nContainer Deposit\n500512\nCAPTAIN MORGAN - SPICED 1X750m\n0.40\n55.98 G\n2 27.99\nContainer Deposit\n144071\nAPEROL BARBIERI APERTIVO 1X750ml\n0.20\n48.98 G\n2 24.49\nContainer Deposit\n0.20\nSubtotal\n446.78\nContainer Deposit Subtotal\nG GST 5%\n2.20\n22.34\n471.32\nTotal\nBC Liquor Store # 160\nAug 08 2019 10:11 amTrans# 017587038351\nTRANSACTION RECORD\nCard:**********4527\nCard Type\nTrans Type\nCard Entry\nAuth\nSequence #\nMerchant ID\nTerminal #\nDate\nTime\n: VI\n:MOTO PURCHASE\nM\n:030518\n:001001906\n: 22111211\n:B42211121117\n:08-08-2019\n:10:11:01\nAmount\n:$471.32\nAPPROVED THANK YOU\nRetain this copy for your\nrecords\n*** CUSTOMER COPY\nTotal Count of Items\n22\nGST Reg #124542945\nYou saved:\n$4.00\nX 10 1601 7 5 8 7 0 3 8 3 5\n1\n"


def get_header_receipt(string):
    first_index = None
    second_index = None
    for index, line in enumerate(string.split('\n')):
        if '*' in line:
            if first_index is None: first_index = index
            elif index - 1 == first_index: continue
            elif second_index is None: second_index = index
            else: break
    return string.split('\n')[first_index:second_index+1]

def clean_header_receipt(list_of_string):
    parse_regex()



# main parsing logic
def parse_regex(string):
    return re.findall(r"^\#.+", string)
    pass

def re_get_bill_from():
    pass

def re_get_bill_to():
    pass

def re_get_bill():
    pass

def re_get_line_items():
    pass


result = re.findall(r"\n.+\n", fullstring_1)
for r in result:
    print(r.replace('\n', ''))

exit()

print(get_header_receipt(fullstring_1))
print(get_header_receipt(fullstring_2))
print(get_header_receipt(fullstring_3))
print(get_header_receipt(fullstring_4))


# exit()

print(parse_regex(fullstring_1))
print(parse_regex(fullstring_2))
print(parse_regex(fullstring_3))
print(parse_regex(fullstring_4))


exit()
