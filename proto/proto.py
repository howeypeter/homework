#!/usr/bin/python
import struct
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
   #enter list of hex and concatenate and convert to decimal
   intOfOutput = ''
   for x in range(begin,end):
     chrctr =  str(list[x])
     intOfOutput = str(intOfOutput + chrctr)
     chrctr = intOfOutput.replace(" ", "")
   return int(intOfOutput, 16)

def parse_transactions(list):
  list_of_transactions = []
  print type(list_of_transactions)
  while len(list) > 40:
    #type 0 - debit 1 - credit 2 - autostart 3- autostop
    transActType = output_range_decimal(0,1,list)
    transActTime = output_range_decimal(1,5,list)
    custID = output_range_decimal(5,13,list)
    del list[0:13]
    if transActType < 2:
      #transActDollars = output_range_decimal(0,9,list)
      transActDollars = output_range_decimal(0,9,list)
      del list[0:8]
    else:
      transActDollars = ''
    transAct = (transActType,transActTime,custID,transActDollars)
    print transAct
    list_of_transactions.append(transAct)
  return list_of_transactions


L = parse_file('txnlog.dat')
print "Begin Headers"
print "System: " + str(output_range_ascii(0,4,L))
print "Version: " + str(output_range_decimal(4,5,L))
print "Number of Records: " + str(output_range_decimal(5,9,L))
print "Begin Transactions"
print parse_transactions(L[9::])
