import java.util.ArrayList;
import java.util.List;

public class Client_Exigeant {

    private List<Client_preference> client_preferences ;
    private int n_potential_clients;

    public Client_Exigeant(){
        this.client_preferences = new ArrayList<>(40);
    }

    public List<Client_preference> getClient_preferences() {
        return client_preferences;
    }

    public void setClient_preferences(List<Client_preference> client_preferences) {
        this.client_preferences = client_preferences;
    }

    public int getN_potential_clients() {
        return n_potential_clients;
    }

    public void setN_potential_clients(int n_potential_clients) {
        this.n_potential_clients = n_potential_clients;
    }
}
