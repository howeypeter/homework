#!/usr/bin/python
import binascii


def parse_file(filename):
# parses the binary file and returns a list of each char in hexadecimal format
   parsedList=[]
   with open(filename, 'rb') as f:
      while f:
         byte_s = f.read(1)
         if not byte_s:
            break
         byte = hex(ord(byte_s))[2:]
	 if len(byte) % 2 == 1:
	    byte = "0" + str(byte)
         parsedList.append(byte)
   return parsedList
def output_range_ascii(begin,end,list):
   stringOfOutput = ''
   for x in range(begin,end):
     chrctr =  list[x]
     chrctr =  binascii.unhexlify(chrctr)
     stringOfOutput = stringOfOutput + str(chrctr)
   return stringOfOutput
def output_range_decimal(begin,end,list):
   stringOfOutput = ''
   for x in range(begin,end):
     chrctr =  list[x]
     chrctr =  int(chrctr, 16)
     stringOfOutput = stringOfOutput + str(chrctr)
   return stringOfOutput
def parse_transactions(list):
  while len(list) > 0:
    transAct = ()
    #type 0 - debit 1 - credit 2 - autostart 3- autostop
    transActType = int(list[0])
    transActTime = output_range_decimal(1,5,list)
    transActID = output_range_decimal(5,14,list)
    print len(list)
    del list[0:13]
    print len(list)
    if transActType < 2:
      transActDollars = output_range_decimal(0,9,list)
      del list[0:8]




L = parse_file('txnlog.dat')
print "Begin Headers"
print "System: " + output_range_ascii(0,4,L)
print "Version: " + output_range_decimal(4,5,L)
print "Number of Records: " + output_range_decimal(5,9,L)
print "Begin Transactions"
parse_transactions(L[9::])
