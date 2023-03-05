import java.io.*;
import java.nio.charset.StandardCharsets;
import java.security.spec.ECGenParameterSpec;
import java.util.Base64;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.*;
import java.util.Scanner;


public class Sign {
    private PrivateKey private_key;
    private PublicKey public_key;
    private String signature_file = "signature.txt";

    public Sign() throws NoSuchAlgorithmException, NoSuchProviderException, InvalidAlgorithmParameterException {

        // Gerar as chaves pública e privada com o NIST P-384 
        KeyPairGenerator generator = KeyPairGenerator.getInstance("EC","SunEC");
        ECGenParameterSpec parameter_spec = new ECGenParameterSpec("secp384r1");
        generator.initialize(parameter_spec);
        KeyPair key_pair = generator.genKeyPair();
        this.private_key = key_pair.getPrivate();
        this.public_key = key_pair.getPublic();
    }

    public byte[] read_file(String filename) throws FileNotFoundException {
        byte[] b = new byte[1];
        try(RandomAccessFile f = new RandomAccessFile(filename, "r")) {
            b = new byte[(int) f.length()];
            f.readFully(b);
        }catch(FileNotFoundException e){
            throw e;
        }catch (IOException e) {
            e.printStackTrace();
        }

        return b;
    }

    public void sign_file(String filename) throws SignatureException, IOException, NoSuchAlgorithmException, NoSuchProviderException, InvalidKeyException {
        // Criar a assinatura com o SHA384 e o provider SunEC
        Signature sign = Signature.getInstance("SHA384withECDSA","SunEC");
        sign.initSign(this.private_key);

        byte[] file  = read_file(filename);
        byte[] signature;

        sign.update(file);
        signature = sign.sign();

        Path path = Paths.get(filename);

        FileWriter fw = new FileWriter(this.signature_file);
        String to_add = "File:" + path + '\n' + "Signature:" + Base64.getEncoder().encodeToString(signature) + '\n';
        fw.append(to_add);
        fw.close();
    }

    public boolean verify_signature(String filename) throws NoSuchAlgorithmException, NoSuchProviderException, InvalidKeyException, SignatureException, IOException {
        File f = new File(this.signature_file);
        FileReader fr = new FileReader(f);
        BufferedReader br = new BufferedReader(fr);
        Path path = Paths.get(filename);
        byte [] signature = new byte[1];

        // Read the signature file line by line
        String line;
        while((line = br.readLine()) != null) {
            String[] first = line.split(":");
            if(first[0].equals("File")){
                if (Paths.get(first[1]).equals(path)){
                    line = br.readLine();
                    String[] second = line.split(":");
                    if(second[0].equals("Signature")){
                        signature = Base64.getDecoder().decode(second[1].getBytes());
                    }
                }
            }
        }
        br.close();

        byte[] file  = read_file(filename);

        Signature sign_instance = Signature.getInstance("SHA384withECDSA","SunEC");
        sign_instance.initVerify(this.public_key);
        sign_instance.update(file);

        return sign_instance.verify(signature);
    }

    public void reset_signatures() throws IOException{
        FileWriter writer = new FileWriter(this.signature_file);
        writer.write("");
        writer.close();
    }

    public static void main(String[] args) throws InvalidAlgorithmParameterException, NoSuchAlgorithmException, NoSuchProviderException, InvalidKeyException, SignatureException, IOException {
        // read the arguments from the command line
        Sign signing = new Sign();

        System.out.println("Choose one operation");
        System.out.println("1 - Sign a file");
        System.out.println("2 - Verify a file signature");
        System.out.println("0 - Leave");

        Scanner sc = new Scanner(System.in);
        int op = Integer.parseInt(sc.next());
        while(op != 0) {
            System.out.println("File name: ");
            String filename = sc.next();

            switch (op) {
                case 1:
                    signing.sign_file(filename);
                    System.out.println("File signed successfully!\n\n");
                    break;
                case 2:
                    if (signing.verify_signature(filename)) {
                        System.out.println("The signature is valid!\n\n");
                    } else System.out.println("The signature is not valid!\n\n");
                    break;
            }
            System.out.println("Choose one operation");
            System.out.println("1 - Sign a file");
            System.out.println("2 - Verify a file signature");
            System.out.println("0 - Leave");

            op = Integer.parseInt(sc.next());
        }
        signing.reset_signatures();
    }
}