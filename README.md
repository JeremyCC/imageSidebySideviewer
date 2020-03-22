# imagecompare
__Python的影像視覺比對工具__  
Distribution of the code is allowd under the License "GNU General Public License v3.0"  
您可在遵守 "GNU General Public License v3.0"的規定下任意使用及散佈這項工具  

__In this tool, you can do 這項工具的功能:__

1.A Synchronized view of multiple images with same size and color channels (Now only support 3 channesl or single channel) 同步顯示多個相同大小及相同數量的色彩通道的影像 (目前僅支援3通道或單通道):
![Image of Syn](https://github.com/JeremyCC/imagecompare/blob/master/Example/SYN.PNG)
![Image of Syn2](https://github.com/JeremyCC/imagecompare/blob/master/Example/SYN2.PNG)


2.Check pixel value (You can define your own text color mapping function based on the value) 查看影像的像素值(您可自定義各數值對應的文字顏色)
![Image of Value](https://github.com/JeremyCC/imagecompare/blob/master/Example/VALUE.PNG)  

3.Check image difference 查看不同影像的差值:

![Image of Diff](https://github.com/JeremyCC/imagecompare/blob/master/Example/SUB.PNG)
![Image of Diff2](https://github.com/JeremyCC/imagecompare/blob/master/Example/SUBALL.PNG)


__Requirement 需求__
> matplotlib>=2.0.2   
> python>=3.5.3  


__How to use 如何使用__  
1.import the tool  
'''python
        import imagecompare
'''
