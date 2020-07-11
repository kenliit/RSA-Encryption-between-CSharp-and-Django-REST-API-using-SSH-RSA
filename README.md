# RSA-Encryption-between-CSharp-and-Django-REST-API-using-SSH-RSA
This is an example about how to encrypt RSA in C# and decrypt in Django Rest Framework using the SSH-RSA key pair generated in Windows 10

# The challenges
1. RSACryptoServiceProvider in C#, the byte order is 'big'. And Crypto in Python, the byte order is 'little'. This mismatch makes the Django Server won't be able to decrypt the messages that have been encrypted in C#.
2. RSACryptoServiceProvider.FromXmlString in C# requires a xml format string instead of a key file.

# My solution
By modifying the public key file for C# end, it makes both ends match the format. therefore, the RSA tunnel will be setting up without problem.

# How to use
1. in Windows 10 computer, use "ssh-keygen" to create the private key("id_rsa" file). If you are not sure how to do, just follow this instruction: https://phoenixnap.com/kb/generate-ssh-key-windows-10

2. Copy the key file("id_rsa" file) to python, put it into the same folder of the "RSAToCSharp.py", run "python RSAToCSharp.py".  the script will be creating "public.xml" file.

3. Add the "public.xml" into the C# project, put it into the base project folder. "Copy to Output Directory" property of this file change to "Copy if newer".  then you are all set.

4. load the "public.xml" with RSACryptoServiceProvider.FromXmlString(), encrypt the string, send it to Django through REST API. Then decrypt the message with "rsa.decrypt" method.  I have showed a sample program here.
