#!/usr/bin/python
import sys
import signal
import struct
import binascii
from optparse import OptionParser

timeout=30

def deadlinehandler(signum, frame):
  print "1"
  sys.exit(1)

def parse_cli():
  ''' CLI parser using OptionParser'''
  parser = OptionParser()
  parser.add_option('-F', '--file',
    dest='filename',
    default='txnlog.dat',
    help='Specify the name of the binary file. Default is txnlog.dat',
    type='string',
    action='store')
  parser.add_option('-T', '--type',
    dest='recordType',
    default=None,
    help='Type of transaction: 0 Debit 1 Credit 2 StartAutoPay 3 StopAutoPay. Usage: -T 0 (Debit)',
    type='int',
    action='store')
  parser.add_option('-A', '--add',
    dest='sumDollars',
    default=False,
    help='Value of total (sum) in dollars, which are Type Debit or Credit',
    action='store_true')
  parser.add_option('-N', '--number',
    dest='number',
    default=False,
    help='Count the number of Debit/Credit/StartAutoPay/StopAutoPay transactions (requires -T type)',
    action='store_true')
  parser.add_option('-C', '--customer',
    dest='customer',
    default=None,
    help='Get balance of a specific customer',
    type='int',
    action='store')
  parser.add_option('-H', '--headers',
    dest='headers',
    default=False,
    help='Output the headers from the file',
    action='store_true')
  return parser.parse_args()

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
  newList = []
  for i in range(0, len(list)):
    blarg =  list[i]
    if blarg[2] == custNo:

      newList.append(blarg)
  return newList

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

def main():
  (options, args) = parse_cli()
  try:
    L = parse_file(options.filename)
    if options.headers == True:
        print "Begin Headers"
        print "System: " + str(output_range_ascii(0,4,L))
        print "Version: " + str(output_range_decimal(4,5,L))
        print "Number of Records: " + str(output_range_decimal(5,9,L))
        return 0
    transactions = parse_transactions(L[9::])
    if options.number == True:
        if options.recordType < 4:
            print "Total Transactions of type " + str(options.recordType) + ": "
            print str(transaction_types(transactions,options.recordType))
            print ""
            return 0
        else:
            print "range must be between 0 and 3"
    if options.sumDollars == True:
        if options.recordType == 0:
            print "Deposits: $" + str(sumDeposits(transactions,options.recordType) )
        elif options.recordType == 1:
            print "Credits: $" + str(sumDeposits(transactions,options.recordType) )
        else:
            print "this will only calculate Debit (0) or Credit (1) transactions"
    if options.customer > 0:
        balance = 0
        trans = find_cust(transactions,options.customer)
        for i in trans:
            if i[0] == 0:
                balance = balance + (i[3] * -1)
            if i[0] == 1:
                balance = balance + i[3]
        print "Customer " + str(options.customer) + " balance: " + str(balance)
  except:
    deadlinehandler(2,3)
  return 0

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, deadlinehandler)
    signal.alarm(timeout)
    exitCode = main()
    print exitCode
    sys.exit(int(exitCode))
    signal.alarm(0)
