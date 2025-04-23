1. 	open powershell as Adminstrator 
	wsl --install

2. 	restart your pc

3. 	Write "ubuntu" on search bar and open it

4. 	create a username and password

5. 	after setup write this to install ollama:
	curl https://ollama.ai/install.sh | sh

6. 	after installed, try a little model:
	ollama run orca-mini

7. 	try asking something to see is it working or not

8. 	press ctrl + d to stop

9. 	type: ollama run deepseek-r1:1.5b

10. after seeing ">>>", press CTRL + D

11.	Now start it in API (server) mode: 
	ollama serve
	Leave this running.

12.	Create Your Python Script in PyCharm or VSCode or etc. (on Windows)

13. run the rag_ollama.py while wsl is running in the background