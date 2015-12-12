# SWE544_2015Fall_Project1
This repository is created for the Project1 assigned in the class SWE544-2015Fall to Sinan Can SÜRÜCÜ

Commits to this project will be detailed in the Commit List, and will be updated within each commit.

Commit List

1) Commit:c54a76c 02/12/2015
    - Repository has been created and first commit has been tried with a readme file

2) Commit:3043bdf 03/12/2015
    - Git integration with PyCharm has been established, committing form the IDE has been tried with an update to ReadME file.
    
3) Commit:4d07c2a 04/12/2015
    - UI with QT Designer has been created, a draft version of the UI has been added to the application.
    - Basic client and server connection has been established without any protocol rule/definitions
    - UX/UI controls and basic features has been added. (e.g. Send button is disabled when message text is empty, Enter button can be used for sending messages in the message text area.)

4) Commit:6e1f3fc 09/12/2015
    - Server connection to 178.233.19.205:12345 has been established, just a dummy one getting TIC message only
    - 2 threads beyond main thread have been added, after running the app, Read and Write threads start
    
5) Commit:81bad12 10/12/2015
    - Threads construction have been changed, because of the while loops, the GUI is frozen so thread mechanism has been revised. In this new version QtCore.QThread is used, and the threads working without blocking the GUI.
    - Queue mechanism has been implemented:
        *  WriteQThread is listening to threadQueue, if threadQueue has any element, it is pushed to the socket.
        *  ReadQThread is listenining to screenQueue, if screenQueue has any element, it is showed in the MessageView of GUI. Any message from server or written in textbox in the GUI, are added to the screenQueue.
    - updateChannelWindow is called if any need to the refreshing the MessageWindow, and this function reads screenQueue and puts it in the MessageView.
    - sendMessage has been implemented, if any message is written in the textbox and press send, the text will be added to the threadQueue and screenqueue.
    
6) Commit:c54a76c 11/12/2015
    - incoming and outgoing parsers are added, more tests and checks will be done on these parsers
    - Online members list is implemented. It is refreshing regularly to get the latest list of the online users.
    - Live test has been executed today. Another student working on the project was online in the system (not planned, we do not know each other also), and we talked for a while on the IRC and tested our applications. 
     
7) Commit: 13/12/2015
    - Hostname/port is taken by command line from user
    - Incoming protocol rules and messages are controlled and fixed
    - Comments has been added in the codes