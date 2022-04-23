import java.util.ArrayList;
import java.util.List;

public class Client_preference {
    private int n_loved_recipes;
    private List<String> loved_recipes = new ArrayList<String>(30);
    private int n_hated_recipes;
    private List<String> hated_recipes = new ArrayList<String>(30);

    public int getN_loved_recipes() {
        return n_loved_recipes;
    }

    public void setN_loved_recipes(int n_loved_recipes) {
        this.n_loved_recipes = n_loved_recipes;
    }

    public List<String> getLoved_recipes() {
        return loved_recipes;
    }

    public void setLoved_recipes(List<String> loved_recipes) {
        this.loved_recipes = loved_recipes;
    }

    public int getN_hated_recipes() {
        return n_hated_recipes;
    }

    public void setN_hated_recipes(int n_hated_recipes) {
        this.n_hated_recipes = n_hated_recipes;
    }

    public List<String> getHated_recipes() {
        return hated_recipes;
    }

    public void setHated_recipes(List<String> hated_recipes) {
        this.hated_recipes = hated_recipes;
    }
}
