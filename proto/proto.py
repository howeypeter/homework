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
    list_of_transactions.append(transAct)
  return list_of_transactions

def find_cust(list,custNo):
  for i in range(0, len(list)):
    blarg =  list[i]
    if blarg[2] == custNo:
      print blarg

def transaction_types(list,idNum):
  #how many of transaction ID 0,1,2,3 ?
  totalNum = 0
  for i in range(0, len(list)):
    blarg =  list[i]
    if blarg[0] == idNum:
      totalNum += 1
  return totalNum

def sumDeposits(list,idNum):
  # sum of all deposits or withdrawals
  totalNum = 0
  for i in range(0, len(list)):
    blarg =  list[i]
    if blarg[0] == idNum:
      totalNum = totalNum + blarg[3]
  return totalNum

L = parse_file('txnlog.dat')
print "Begin Headers"
print "System: " + str(output_range_ascii(0,4,L))
print "Version: " + str(output_range_decimal(4,5,L))
print "Number of Records: " + str(output_range_decimal(5,9,L))
print "Begin Transactions"
transactions = parse_transactions(L[9::])
#print find_cust(transactions,2456938384156277127)
print "total autopays stopped: " + str(transaction_types(transactions,3) )
print "total autopays started: " + str(transaction_types(transactions,2) )
print "total deposits: " + str(sumDeposits(transactions,0) )
print "total withdrawals: " + str(sumDeposits(transactions,1) )
