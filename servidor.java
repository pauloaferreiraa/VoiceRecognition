/**
 * Created by vitor on 20-06-2017.
 */
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class servidor{

    public static void main(String[] args){

        try {
            ServerSocket server_Socket = new ServerSocket(8421); //cria socket e da bind na porta 4444
            Socket client_Socket = server_Socket.accept(); // aceita a coneção que vem do cliente e fica à espera até
                                                           // receber esse pedido de coneção
            PrintWriter out = new PrintWriter(client_Socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(client_Socket.getInputStream()));

            String s = in.readLine();               
            System.out.println(s);
            while(true) {                
                s = in.readLine(); 
                if(s == null) break;          
                System.out.println(s);
                out.println("OK");
                out.flush();
            }
        }catch(Exception e){
            e.printStackTrace();
        }



    }
}
