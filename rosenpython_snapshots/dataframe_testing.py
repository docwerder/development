import pandas as pd

if __name__ == '__main__':
    df = pd.DataFrame()
    print(df)
    df["counts"] = [10, 20, 30, 40]
    df["anom_types"] = ["MELO", "OTHER", "LIN", "CRAC"]
    print(df)
    df["names"] = ["FERKEG"] * len(df["counts"])
    #% Wichtig sind hier die []... Weil dann wird der Begriff als Liste angesehen...
    #% Und mit len.. wird entspechend jeder Eintrag multipliziert... und dann 
    #% als Liste in der Tabellenspalte df["names"] gesetzt..

    # print(df)

    df_tmp_2 = pd.DataFrame()
    df_tmp_2["counts"] = [555, 100]
    df_tmp_2["anom_types"] = ["PIFE-NOTC", "COAT-IMP"]
    df_tmp_2["names"] = ["FERKEG"] * len(df_tmp_2["counts"])

    df_3 = [df, df_tmp_2]
    print(df_3)