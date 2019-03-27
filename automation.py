import os
import re
global bitrate_list
import matplotlib.pyplot as plt
def addvideo_encoding(input1,input2):
    file1=input1
    file2=input2
    bitrate=input('Enter the bitrate')
    bitrate_list.append(bitrate)
    nameoutput_264='{0}_{1}_h264.mp4'.format(file2,bitrate)
    nameoutput_265='{0}_{1}_h265.mp4'.format(file2,bitrate)
    nameoutput_vp9='{0}_{1}_vp9.mp4'.format(file2,bitrate)

    os.system('/usr/bin/time -f \'time: %E\' -a -o 264time.txt ./ffmpeg -i {0} -c:v libx264 -b {1} {2}'.format(file1, bitrate, nameoutput_264))
    os.system('/usr/bin/time -f \'time: %E\' -a -o 265time.txt ./ffmpeg -i {0} -c:v libx265 -b {1} {2}'.format(file1, bitrate, nameoutput_265))
    os.system('/usr/bin/time -f \'time: %E\' -a -o vp9time.txt ./ffmpeg -i {0} -c:v libvpx-vp9 -b {1} {2}'.format(file1, bitrate, nameoutput_vp9))

def testvmaf(x,y,z,l):
    encoder_type=x
    filename=y
    simplename=z
    bitratevalue=bitrate_list[l]
    command='./ffmpeg -i {0}_{1}_{2}.mp4 -i {3} -lavfi libvmaf="model_path=./model/vmaf_v0.6.1.pkl:psnr=1:log_fmt=json" -f null -'.format(simplename,bitratevalue,encoder_type,filename)
    r=os.popen(command)
    info=r.readlines()
    text=r'vmaf1.txt'
    fhandle=open(text,'w') 
    for line in info:
        fhandle.writelines(str(line))
        line=line.strip('\r\n')
        print (line)
    fhandle.close()  



if __name__ == '__main__':
    x=input('Do you want to add a file to be encoded?y/n')
    bitrate_list=[]
    nameinput=input('Enter the video file name')
    simple_name=input('Enter the simple name')
    l=input('1.H.264 H.265 VP9 measurement\n2.AV1measurement\n3.Exit\n1or2or3')
    while 1:
        if (l=='1'):
            while x=='y':
                addvideo_encoding(nameinput,simple_name)
                x=input('Do you want to add a file to be encoded?y/n')
            timelist_264=[]
            read_time1=open('264time.txt','r')
            for line in read_time1:
                line=line.replace('\n','').split(' ')
                timelist_264.append(line[1])
            read_time1.close()
            open('264time.txt','w').close()
            print(timelist_264) 
            realtime_264=[]
            for t in timelist_264:
                times = list(map(float, re.split(r"[:]", t)))
                realtime_264.append(times[0]*60+times[1])
                print (times[0]*60+times[1])
            print(realtime_264)
    
            timelist_265=[]
            read_time2=open('265time.txt','r')
            for line in read_time2:
                line=line.replace('\n','').split(' ')
                timelist_265.append(line[1])
            read_time2.close()
            open('265time.txt','w').close()
            print(timelist_265) 
            realtime_265=[]
            for t in timelist_265:
                times = list(map(float, re.split(r"[:]", t)))
                realtime_265.append(times[0]*60+times[1])
                print (times[0]*60+times[1])
            print(realtime_265)

            timelist_vp9=[]
            read_time3=open('vp9time.txt','r')
            for line in read_time3:
                line=line.replace('\n','').split(' ')
                timelist_vp9.append(line[1])
            read_time3.close()
            open('vp9time.txt','w').close()
            print(timelist_vp9) 
            realtime_vp9=[]
            for t in timelist_vp9:
                times = list(map(float, re.split(r"[:]", t)))
                realtime_vp9.append(times[0]*60+times[1])
                print (times[0]*60+times[1])
            print(realtime_vp9)    
    
            Fbitrate_list=[]    
            for num in bitrate_list:
                Fbitrate_list.append(float(num))   
            print(Fbitrate_list)
        
            plt.figure()
            plt.xlabel('bitrate')
            plt.ylabel('encoding time')
            plt.plot(bitrate_list,realtime_264,label='H264',color='r')
            plt.plot(bitrate_list,realtime_265,label='HEVC',color='g')
            plt.plot(bitrate_list,realtime_vp9,label='VP9',color='b')

            plt.legend(loc='best')
            plt.show
            vmaflist_h264=[]
            vmaf264_float=[]
            n=0
            while n<len(bitrate_list):
                testvmaf('h264',nameinput,simple_name,n)
                b=open('vmaf1.txt','r').readlines()
                line2=b[2].replace('\n','').split(' ')
                vmaflist_h264.append(line2[3])  
                n=n+1
            for num in vmaflist_h264:
                vmaf264_float.append(float(num))
            print(vmaf264_float)

            vmaflist_h265=[]
            vmaf265_float=[]
            n1=0
            while n1<len(bitrate_list):
                testvmaf('h265',nameinput,simple_name,n1)
                b=open('vmaf1.txt','r').readlines()
                line2=b[2].replace('\n','').split(' ')
                vmaflist_h265.append(line2[3])  
                n1=n1+1
            for num in vmaflist_h265:
                vmaf265_float.append(float(num))
            print(vmaf265_float)    

            vmaflist_vp9=[]
            vmafvp9_float=[]
            n2=0
            while n2<len(bitrate_list):
                testvmaf('vp9',nameinput,simple_name,n2)
                b=open('vmaf1.txt','r').readlines()
                line2=b[2].replace('\n','').split(' ')
                vmaflist_vp9.append(line2[3])  
                n2=n2+1
            for num in vmaflist_vp9:
                vmafvp9_float.append(float(num))
            print(vmafvp9_float)     
    
            plt.figure()
            plt.xlabel('bitrate')
            plt.ylabel('vmaf')

            plt.plot(bitrate_list,vmaf264_float,label='H264',color='r')
            plt.plot(bitrate_list,vmaf265_float,label='HEVC',color='g')
            plt.plot(bitrate_list,vmafvp9_float,label='VP9',color='b')
            plt.legend(loc='best')
            plt.show
            print(realtime_264)
            print(realtime_265)
            print(realtime_vp9)
            print(vmaf264_float)
            print(vmaf265_float)
            print(vmafvp9_float)
            print(Fbitrate_list)
            l=input('try other options 2,3')
        if(l=='2'):
            bitrate_av1=input('Enter bitrate')
            av1_output='{0}_{1}_AV1.mp4'.format(simple_name,bitrate_av1)
            os.system('/usr/bin/time -f \'time: %E\' -a -o outAV1.txt ./ffmpeg -i {0} -c:v libaom-av1 -b:v {1} -strict experimental {2}'.format(nameinput,bitrate_av1,av1_output))
            timelist_av1=[]
            read_time4=open('outAV1.txt','r')
            for line in read_time4:
                line=line.replace('\n','').split(' ')
                timelist_av1.append(line[1])
            read_time4.close()
            open('outAV1.txt','w').close()
            realtime_av1=[]
            for t in timelist_av1:
                times = list(map(float, re.split(r"[:]", t)))
                realtime_av1.append(times[0]*60+times[1])
                print (times[0]*60+times[1])
            print(realtime_av1)
            os.system('./ffmpeg -i {0} -i {1} -lavfi libvmaf="model_path=./model/vmaf_v0.6.1.pkl:psnr=1:log_fmt=json" -f null -'.format(av1_output,nameinput))
            l=input('try other options1,3')
        if(l=='3'):
            break
        else:
            l=input('try again')
        
            
    
    
    
    
    
    
    
    
    
    
    
    
