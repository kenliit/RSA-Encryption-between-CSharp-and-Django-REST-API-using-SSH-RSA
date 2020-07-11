using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace TestRSA2
{
    class Program
    {
        public static void Main(string[] args)
        {
            RSACryptoServiceProvider csp = new RSACryptoServiceProvider(2048);
            csp.FromXmlString(File.ReadAllText("./public.xml"));

            // encrypting a string for testing purposes
            byte[] plainText = Encoding.ASCII.GetBytes("Hello from CSharp");
            byte[] cipherText = csp.Encrypt(plainText, false);

            Console.WriteLine("Encrypted: " + Convert.ToBase64String(cipherText));
            Console.ReadKey();
        }
    }
}
