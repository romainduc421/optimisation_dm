public class Ing_all {
    private boolean isLoved;
    private String name_recipe;
    private int clientID;
    public Ing_all(int clientID, String name_recipe, boolean isLoved){
        this.clientID = clientID;
        this.name_recipe = name_recipe;
        this.isLoved = isLoved;
    }

    public boolean isLoved() {
        return isLoved;
    }

    public void setLoved(boolean loved) {
        isLoved = loved;
    }

    public String getName_recipe() {
        return name_recipe;
    }

    public void setName_recipe(String name_recipe) {
        this.name_recipe = name_recipe;
    }

    public int getClientID() {
        return clientID;
    }

    public void setClientID(int clientID) {
        this.clientID = clientID;
    }
}
