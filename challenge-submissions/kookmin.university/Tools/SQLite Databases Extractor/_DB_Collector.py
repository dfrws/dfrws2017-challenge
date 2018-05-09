 # -*- coding: utf8 -*-

__author__ = "DF&C"

import sys
from collections import OrderedDict
import string


 #import class_directory_entry.py#

#some a = Directory_entry(filename)
class Directory_entry:
    def __init__(self,filename):
        #self.filename = filename
        self.f=open(filename,'rb')
        self.ext4_list=[]
        self.partition_tmp=0
        #root={}
        self.lines=[]
        self.data_dict={}
        b_n=1
        #extents,block_cum
        del self.lines[0:len(self.lines)]
        #################################
        #                               #
        #################################
        self.Partition_Find()
        
        for self.label in range(len(self.ext4_list)):
            item = self.SBGD(0)
            self.SGD =item[0]
            self.IPG =item[1]
            self.GDB =item[2]
            offset = item[3]
            course =''
            self.Entry_view(course,offset,b_n)

    def Partition_Find(self):
        self.f.seek(0x1fe)
        MBR=self.f.read(2)
        MBR_part_info=[]
        if ord(MBR[0])==0x55 and ord(MBR[1])==0xAA:
            self.f.seek(0x1be)
            for x in range(0,4):
                partition_info=self.f.read(0x10)
                partition_info=(ord(partition_info[8]))^ (ord(partition_info[9])<<8) ^(ord(partition_info[10])<<16) ^(ord(partition_info[11])<<24)
                if partition_info!=0x0:
                    MBR_part_info.append(partition_info*0x200)
                    
            
            for info in MBR_part_info:
                #print '%x'%(info/0x200)
                self.f.seek(info+0x438)
                tmp=self.f.read(2)
                if ord(tmp[0])==0x53 and ord(tmp[1])==0xEF:self.ext4_list.append(info)
        else:
            self.ext4_list.append(0x0)

        

    def export_data(self):
        return (self.lines , self.data_dict, self.SGD, self.IPG, self.GDB, self.ext4_list)

    def exit(self):
        self.name_dict.clear()
        self.data_dict.clear()
        self.f.close

    def SBGD(self,offset):

        #print self.ext4_list
        self.partition_tmp=self.ext4_list[0]

        self.f.seek(0)
        item_list=[]
        while True:
            self.f.seek(offset+self.partition_tmp)
            self.f.seek(0x28,1)
            IPG=self.f.read(4)
            self.f.seek(0xC,1)
            data=self.f.read(2)
            if (ord(data[0])==0x53 and ord(data[1])==0xef):
                if(offset%0x400 == 0):
                    GDB = offset+0xC00+self.partition_tmp
                    break
                elif(offset%0x1000 == 0):
                    GDB = offset+0x1000+self.partition_tmp
                    break
            offset+=0x200
        self.f.seek(0xC4,1) # Magic Signature+C4 = FE = Size of Group Discriptor
        SGD=self.f.read(2)
        SGD=(ord(SGD[0]))^(ord(SGD[1])<<8)
        IPG=(ord(IPG[0]))^(ord(IPG[1])<<8)^(ord(IPG[2])<<16)^(ord(IPG[3])<<24)
        #Super block end  && Group Descriptor Start
        self.f.seek(GDB)
        if SGD==0x20 or SGD==0x00:
            SGD=0x20
            self.f.seek(0x8,1)
            data=self.f.read(4)
            lendata=len(data)
            result=0
            for i in range(lendata):
                result^=(ord(data[i])<<i*8)
            result = result *0x1000+0x100
        elif SGD==0x40:
            print '...' 
            result = 0 
    #########################################################################################################
    ##########################################################################################################
        ##########################################################################################################
            ##########################################################################################################


        self.f.seek(result+self.partition_tmp)
        self.f.seek(0x3A,1)
        data=self.f.read(6)
        lendata=len(data)
        n_offset=0
        for i in range(lendata):
            n_offset^=(ord(data[(lendata+1-i)%lendata])<<(((lendata-1)*8)-8*i))
        item_list.append(SGD)
        item_list.append(IPG)
        item_list.append(GDB)
        item_list.append(n_offset*0x1000+self.partition_tmp)
        return item_list

        

    def depth_f(self,offset,b_n_offset):
        internal_offset=[]
        self.f.seek(offset)
        data=self.f.read(12)
        if(ord(data[0])!=0x0A and (ord(data[1])!=0xF3)):
            return 0
        depth=ord(data[6])^(ord(data[7])<<8)
        if (depth ==0 ):
            leaf_num=ord(data[2])^(ord(data[3])<<8)
            while leaf_num>0:
                exdata=self.f.read(6)
                blockcount=ord(exdata[4])^(ord(exdata[5])<<8)
                exdata=self.f.read(6)
                lenexdata=len(exdata)
                n_offset=0
                for i in range(lenexdata):
                    n_offset^=(ord(exdata[(lenexdata+1-i)%lenexdata])<<(((lenexdata-1)*8)-8*i))
                n_offset=n_offset*0x1000+self.partition_tmp
                b_n_offset.append(str(blockcount)+'_'+str(n_offset))
                leaf_num-=1
        else:
            internal_num=ord(data[2])^(ord(data[3])<<8)
            while internal_num>0:
                n_offset=0
                internaldata=self.f.read(12)
                n_offset=(ord(internaldata[9])<<40)^(ord(internaldata[8])<<32)^(ord(internaldata[7])<<24)^(ord(internaldata[6])<<16)^(ord(internaldata[5])<<8)^(ord(internaldata[4]))
                n_offset=n_offset*0x1000+self.partition_tmp
                internal_offset.append(n_offset)
                internal_num-=1
            for i in range(len(internal_offset)):
                self.depth_f(internal_offset[i],b_n_offset)
       



    def InodeTable(self,inode):
        ###################################################
        #  calc grub discriptor and offset of InodeTable  #
        blocknum=(inode-1)/self.IPG
        inodeT=(inode%self.IPG)-1
        self.f.seek(self.GDB+(blocknum*self.SGD)+0x08)
        readTable=self.f.read(4)
        readTable=(ord(readTable[0]))^(ord(readTable[1])<<8)^(ord(readTable[2])<<16)^(ord(readTable[3])<<24)
        readTable=(readTable*0x1000) + (inodeT*0x100)+self.partition_tmp
        ####################################################
        #                in Inode Table                    #
        b_n_offset=[]
        self.depth_f(readTable+0x28,b_n_offset)
        return b_n_offset
        # inode table의 offset , block개수 반환

        # b_n_offset=[]
        # self.depth_f(readTable+0x28,b_n_offset)
        # #######################################################################
        # offset=0
        # for i in range(len(b_n_offset)):
        
        #return (offset , bn_extent)

    def Entry_view(self,course,offset,b_n):
        #print self.label
        in_label='%s'%self.label#'partition_'+'%s'%self.label
        i=0
        self.f.seek(offset)
        count = 0x00

        while True:
            inode = self.f.read(4)
            data = self.f.read(4)
            entry=((ord(data[1])<<8) ^ ord(data[0]))


            namelen = ord(data[2])
            name = self.f.read(namelen)
            inode=(ord(inode[0]))^(ord(inode[1])<<8)^(ord(inode[2])<<16)^(ord(inode[3])<<24)
            count+=entry

            # if name=='timezone' or name=='clock':
            #     print course
            #db_list=['db','mdb','accdb','adp','dbf','database']
            # if name == "88:0F:10:F6:C8:B7":
            #     print 'here'

            if namelen==0:break
                    
            if i>1:
                #if name[-3:]=='.db' or name[-3:]=='.mdb':
                #if name.split('/')[-1:][0] in db_list or name.split('.')[-1:][0] in db_list :
                self.data_dict[inode]=in_label+course+'/'+name
                self.lines.append(in_label+course+'/'+name)


                if ord(data[3])==0x2:
                    cal=self.InodeTable(inode)
                    #cal[i] = str blockcount _ str n_offset 으로이루어짐
                    for j in range(len(cal)):
                        calbn=int(cal[j].split('_')[0])
                        caloffset=int(cal[j].split('_')[1])
                        
                        
                        self.Entry_view(course+'/'+name,caloffset,calbn)

            if count>= 0x1000*b_n:break

            i+=1
            self.f.seek(offset+count)

#a=Directory_entry('E:/001-SmartTV-RaspberryPi/SMARTVMMC')

#a=Directory_entry('D:/002-BettyNote2Black/002-BettyNote2Black/SHV-E250L_Physical_20170717/SHV-E250L_Physical_20170717_USERDATA.mdf')