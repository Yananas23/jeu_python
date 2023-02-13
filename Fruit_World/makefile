td3: main.o 
		gcc -o td3 main.o 

main.o: python2csharp.cs
		gcc -c python2csharp.cs


ifneq ($(OS),Windows_NT)
clean:
		rm -f *.o
else
clean:
	  	del /f /q *.o
endif

all:
		make td3
		make clean