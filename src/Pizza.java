import java.util.ArrayList;
import java.util.List;

public class Pizza {
    private int n_recipes;
    private List<String> recipes_name_list = new ArrayList<>(30);

    public int getN_recipes() {
        return n_recipes;
    }

    public void setN_recipes(int n_recipes) {
        this.n_recipes = n_recipes;
    }

    public List<String> getRecipes_name_list() {
        return recipes_name_list;
    }

    public void setRecipes_name_list(List<String> recipes_name_list) {
        this.recipes_name_list = recipes_name_list;
    }
}
