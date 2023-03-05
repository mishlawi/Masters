/**
 * necessary imports for the running the program
 */
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.ByteBuffer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Scanner;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class AES128GCM {

    // the name of the transformation to apply in the cipher
    private static final String ENCRYPT_ALGO = "AES/GCM/NoPadding";
    // tag size in bits
    private static final int TAG_LENGTH_BIT = 128;
    // initial vector size in bytes
    private static final int IV_LENGTH_BYTE = 12;
    // key size in bits 
    private static final int KEY_SIZE_BITS = 128;

    // private static final Charset UTF_8 = StandardCharsets.UTF_8;

    private static Scanner sc = new Scanner(System.in);

    private static String key;
    private static String operation;
    private static String fromFile;
    private static String toFile;

    /**
     * main fucntion
     * 
     * @param args
     */
    public static void main(String[] args) {
        
        // read the arguments from the command line
        try{
            if(args.length == 3){
                System.out.println("Please enter the key: ");
                key = sc.nextLine();
                System.out.println(key.getBytes("UTF-8").length);
                while(!(key.getBytes("UTF-8").length == 16)){
                    System.out.println("Please enter a 16 bytes (128 bits) key: ");
                    key = sc.nextLine();
                }
                operation = args[0];
                fromFile = args[1];
                toFile = args[2];
            }
            else{
                key = args[0];
                while(!(key.getBytes("UTF-8").length == 16)){
                    System.out.println("Please enter a 16 bytes (128 bits) key: ");
                    key = sc.nextLine();
                }
                operation = args[1];
                fromFile = args[2];
                toFile = args[3];
            }
            
        } catch(Exception e){
            e.printStackTrace();
            System.out.println("Please enter the key, the operation to execute (encrypt/decrypt), the input file path and the output file path as arguments of the program");
        }
        
        
        if(operation.equals("encrypt")){
            // read the input txt file
            byte[] fileContent = null;
            try {
                fileContent = Files.readAllBytes(Paths.get(ClassLoader.getSystemResource(fromFile).toURI()));
            } catch (IOException | URISyntaxException e1) {
                e1.printStackTrace();
            }

            // get a SecretKey instance with the key entered by the user
            SecretKey secretKey = null;
            try {
                secretKey = AES128GCM.getAESKeyFromKey(key);
            } catch (NoSuchAlgorithmException e) {
                e.printStackTrace();
            }

            // compute the initial vector
            byte[] iv = AES128GCM.getRandomNonce(IV_LENGTH_BYTE);

            // encrypt the text and add the initial vector to it
            byte[] encryptedText = new byte[0];
            try {
                encryptedText = AES128GCM.encryptWithPrefixIV(fileContent, secretKey, iv);
            } catch (Exception e) {
                e.printStackTrace();
            }
            
            Path path = Paths.get(toFile);

            // write the result from the encryption on a file named by the user
            try {
                Files.write(path, encryptedText);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else{
            if(operation.equals("decrypt")){
                
                // get a SecretKey instance with the key entered by the user
                SecretKey secretKey = null;
                try {
                    secretKey = AES128GCM.getAESKeyFromKey(key);
                } catch (NoSuchAlgorithmException e) {
                    e.printStackTrace();
                }

                // read the input txt file
                byte[] fileEncryptedText = new byte[0];
                try {
                    fileEncryptedText = Files.readAllBytes(Paths.get(fromFile));
                } catch (IOException e) {
                    e.printStackTrace();
                }

                // decrypt the text unpacking the bytes to find the initial vector and tag
                byte[] decryptedText = new byte[0];
                try {
                    decryptedText = AES128GCM.decryptWithPrefixIV(fileEncryptedText, secretKey);
                } catch (Exception e) {
                    e.printStackTrace();
                }

                Path path = Paths.get(toFile);
                
                // write the result from the decryption on a file named by the user
                try {
                    Files.write(path, decryptedText);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }


    /**
     * encryption method
     * 
     * @param pText
     * @param secret
     * @param iv
     * @return
     * @throws Exception
     */
    public static byte[] encrypt(byte[] pText, SecretKey secret, byte[] iv) throws Exception {

        // get an instance with the specified transformation - "AES/GCM/NoPadding"
        Cipher cipher = Cipher.getInstance(ENCRYPT_ALGO);
        // initialize the cipher with encryption mode 
        // and passing the tag length and iv buffer to create GCMParameterSpec  
        cipher.init(Cipher.ENCRYPT_MODE, secret, new GCMParameterSpec(TAG_LENGTH_BIT, iv));
        // cipher the text
        byte[] encryptedText = cipher.doFinal(pText);
        return encryptedText;

    }

    /**
     * prefix IV length + IV bytes to cipher text
     * 
     * @param pText
     * @param secret
     * @param iv
     * @return
     * @throws Exception
     */
    public static byte[] encryptWithPrefixIV(byte[] pText, SecretKey secret, byte[] iv) throws Exception {

        // get the ciphered text
        byte[] cipherText = encrypt(pText, secret, iv);

        // add the initial vector to the "string"
        byte[] cipherTextWithIv = ByteBuffer.allocate(iv.length + cipherText.length)
                .put(iv)
                .put(cipherText)
                .array();
        return cipherTextWithIv;

    }

    /**
     * 
     * @param cText
     * @param secret
     * @param iv
     * @return
     * @throws Exception
     */
    public static byte[] decrypt(byte[] cText, SecretKey secret, byte[] iv) throws Exception {

        // get an instance with the specified transformation - "AES/GCM/NoPadding"
        Cipher cipher = Cipher.getInstance(ENCRYPT_ALGO);
        // initialize the cipher with decrypting mode 
        cipher.init(Cipher.DECRYPT_MODE, secret, new GCMParameterSpec(TAG_LENGTH_BIT, iv));
        // decipher the text
        byte[] plainText = cipher.doFinal(cText);
        return plainText;

    }

    /**
     * 
     * @param cText
     * @param secret
     * @return
     * @throws Exception
     */
    public static byte[] decryptWithPrefixIV(byte[] cText, SecretKey secret) throws Exception {

        ByteBuffer bb = ByteBuffer.wrap(cText);
        byte[] iv = new byte[IV_LENGTH_BYTE];
        
        // get the initial vector from the text in the file
        bb.get(iv);

        byte[] cipherText = new byte[bb.remaining()];
        // get the ciphered text
        bb.get(cipherText);

        // decipher the text
        return decrypt(cipherText, secret, iv);

    }

    /**
     * get a random initial vector with the SecureRandom package
     *  12 bytes IV
     * 
     * @param numBytes
     * @return
     */
    public static byte[] getRandomNonce(int numBytes) {
        byte[] nonce = new byte[numBytes];
        new SecureRandom().nextBytes(nonce);
        return nonce;
    }

    /**
     * get an instance of SecretKey from a String given by the user
     * 
     * @param key
     * @return
     * @throws NoSuchAlgorithmException
     */
    public static SecretKey getAESKeyFromKey(String key) throws NoSuchAlgorithmException {
        byte[] encodedKey = key.getBytes();
        return new SecretKeySpec(encodedKey, 0, encodedKey.length, "AES");
    }

    /**
     * generates a SecretKey of size 'keysize' which is given
     * 
     * @param keysize
     * @return
     * @throws NoSuchAlgorithmException
     */
    public static SecretKey getAESKey() throws NoSuchAlgorithmException {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(KEY_SIZE_BITS, SecureRandom.getInstanceStrong());
        return keyGen.generateKey();
    }

}