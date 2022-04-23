
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;


public class Main {

    public static String path="src/soluce/";
    /*
    * liste des noms des ingrédients avec nb de fois où il est aimé/détesté ainsi que si l'ingrédient est sélectionné
    * */
    public static List<Ingredient_info> myrecipes_info_list = new ArrayList<Ingredient_info>();
    /*
    * liste des noms des ingrédients associés à l'id du client ainsi qu'un booleen qui indique si le client aime ou non cet ingrédient
    * */
    public static List<Ing_all> myrecipes_all_list = new ArrayList<Ing_all>();
    /*
    * liste des fichiers à traiter en entrée
    * */
    public static List<String> filenamesList = new ArrayList<String>();

    /**
     *
     * @param client_exigeant liste des préférences du client
     * @return pizza avec n ingrédients
     */
    public static Pizza creerPizza(Client_Exigeant client_exigeant)
    {
        Pizza p = new Pizza();

        System.out.println("#Loved = "+myrecipes_info_list.stream()
                .filter(pi-> pi.isSelected()).count()
        +" - # Hated = "+myrecipes_info_list.stream()
                .filter(pi-> !pi.isSelected()).count());


        p.getRecipes_name_list().addAll(myrecipes_info_list.stream().filter(pi->pi.isSelected()).map(pi->pi.getName_recipe()).collect(Collectors.toList()));
        p.setN_recipes(p.getRecipes_name_list().size());
        return p;
    }

    /**
     *
     * @param fullPath chemin absolu/relatif des entrées
     * @return
     * @throws IOException
     */
    public static Client_Exigeant readInput(String fullPath) throws IOException {
        Client_Exigeant client_exigeant = new Client_Exigeant();
        System.out.println(Paths.get(fullPath).toAbsolutePath());
        final List<String> myInputfile = Files.readAllLines(Paths.get(fullPath), StandardCharsets.UTF_8);

        client_exigeant.setN_potential_clients(Integer.parseInt(myInputfile.get(0)));

        for(int k=1; k<=client_exigeant.getN_potential_clients()*2; k+=2 )
        {
            String[] loved_ing_line = myInputfile.get(k).split(" ");
            String[] hated_ing_line = myInputfile.get(k+1).split(" ");

            /* for e_elabore.txt, if you filter out cients who hate more than 3 recipes you get a better score
            but that's not the case for the d_difficile.txt
            * */
            if(!fullPath.contains("elabore") || (fullPath.contains("elabore") && Integer.parseInt(hated_ing_line[0]) < 3)){
                Client_preference client_preference = new Client_preference();
                client_preference.setN_loved_recipes(Integer.parseInt(loved_ing_line[0]));

                for(int l=1; l<= client_preference.getN_loved_recipes(); l++)
                {
                    client_preference.getLoved_recipes().add(loved_ing_line[l]);
                    myrecipes_all_list.add(new Ing_all(k, loved_ing_line[l],true ));
                }

                client_preference.setN_hated_recipes(Integer.parseInt(hated_ing_line[0]));
                for(int l=1; l<= client_preference.getN_hated_recipes(); l++)
                {
                    client_preference.getHated_recipes().add(hated_ing_line[l]);
                    myrecipes_all_list.add(new Ing_all(k, hated_ing_line[l],false ));
                }

                client_exigeant.getClient_preferences().add(client_preference);
                System.out.println(((double)client_exigeant.getClient_preferences().size()/(double)client_exigeant.getN_potential_clients())*100+"% read");
            }
        }

        List<Ingredient_info> res = new ArrayList<>();
        for(Ing_all ing_info : myrecipes_all_list){
            String ing_n = ing_info.getName_recipe();
            int n_lov = (int) myrecipes_all_list.stream().filter(p-> p.getName_recipe().equals(ing_info.getName_recipe()) && p.isLoved()).count();
            int n_hat = (int) myrecipes_all_list.stream().filter(p-> p.getName_recipe().equals(ing_info.getName_recipe()) && !p.isLoved()).count();
            res.add(new Ingredient_info(ing_n, n_lov, n_hat));
        }

        for(Ingredient_info item : res)
        {
            if(myrecipes_info_list.stream().filter(p->p.getName_recipe().equals(item.getName_recipe())).count() == 0)
            {
                myrecipes_info_list.add(new Ingredient_info(item.getName_recipe(), item.getN_loved(), item.getN_hated()));
            }
        }

        return client_exigeant;
    }

    /**
     *
     * @param p
     * @param fullPath chemin absolu/relatif des entrées
     * @throws IOException
     */
    public static void writeOutput(Pizza p, String fullPath) throws IOException {
        StringBuilder txt = new StringBuilder(10).append(p.getN_recipes());

        for(String s : p.getRecipes_name_list())
            txt.append(" ").append(s);


        String res = txt.toString();
        String[] path_sp = fullPath.split("\\.");


        Files.writeString(Path.of(path_sp[0] + "_solution."+path_sp[1]), res, StandardCharsets.UTF_8);
    }

    public static void main(String[] args) {
        filenamesList.add("a_exemple.txt");
        filenamesList.add("b_basique.txt");
        filenamesList.add("c_grossier.txt");
        //filenamesList.add("d_difficile.txt");
        filenamesList.add("e_elabore.txt");

        for(String myfilename : filenamesList)
        {
            myrecipes_info_list = new ArrayList<Ingredient_info>();
            myrecipes_all_list = new ArrayList<Ing_all>();

            Client_Exigeant client_exigeant = new Client_Exigeant();
            System.out.println("- Start Reading - "+myfilename);
            try {
                client_exigeant = readInput(path+myfilename);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            Pizza myp = creerPizza(client_exigeant);
            try {
                writeOutput(myp, path+myfilename);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

            System.out.println("N of selected ing = "+myp.getN_recipes()+"\n- Finished Running - "+myfilename);

        }
    }
}