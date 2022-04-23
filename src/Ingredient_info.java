public class Ingredient_info {
    private String name_recipe;
    private int n_loved;
    private int n_hated;
    private boolean isSelected;
    public Ingredient_info(String nom, int n_loved, int n_hated)
    {
        this.n_hated = n_hated;
        this.n_loved = n_loved;
        double loved_to_hate = this.n_hated==0? 10 : (double)n_loved / (double) n_hated;
        isSelected = loved_to_hate>=1;
        name_recipe = nom;
    }

    public String getName_recipe() {
        return name_recipe;
    }

    public void setName_recipe(String name_recipe) {
        this.name_recipe = name_recipe;
    }

    public int getN_loved() {
        return n_loved;
    }

    public void setN_loved(int n_loved) {
        this.n_loved = n_loved;
    }

    public int getN_hated() {
        return n_hated;
    }

    public void setN_hated(int n_hated) {
        this.n_hated = n_hated;
    }

    public boolean isSelected() {
        return isSelected;
    }

    public void setSelected(boolean selected) {
        isSelected = selected;
    }
}
