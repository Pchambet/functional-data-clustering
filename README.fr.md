# functional-data-clustering — version française

*English version: [README.md](README.md).*

Classification non supervisée de données mixtes : chaque individu est décrit à la fois par une
**courbe** (partie fonctionnelle, dans $L^2$) et par un **vecteur de covariables** (dans
$\mathbb{R}^p$). Comment fusionner les deux pour former des groupes, et peut-on régler cette
fusion sans étiquettes ? Projet long du Master TRIED, CNAM (laboratoire CEDRIC, équipe MSDMA),
2026, proposé et encadré par V. Audigier, F. Bouhadjera et N. Niang. Le mémoire complet :
[`docs/rapport_stage.pdf`](docs/rapport_stage.pdf).

![Silhouette contre meilleur ARI atteignable sur trois jeux étiquetés](docs/figures/hero_silhouette_gap.png)

## En bref

- **Le réglage par silhouette est le verrou.** Choisir les poids courbe/covariables (α, ω) de la
  distance pondérée $D_w$ par la silhouette mène, sur les trois jeux réels, à un coin
  mono-modalité et à un ARI bien inférieur à ce que la même grille permet :
  0,616 contre 0,898 (Canadian Weather), 0,424 contre 0,756 (Berkeley Growth),
  0,151 contre 0,626 (Tecator).
- **Aucune géométrie ne domine partout.** Sur données réelles, le meilleur ARI vient de la fusion
  la plus simple, scores FPCA + covariables puis k-means (0,748 et 0,682), ou des seules
  covariables sur Tecator (0,546).
- **Simulation (4 scénarios × 50 graines, n = 300, k = 3).** Le produit de noyaux gaussiens
  obtient le meilleur ARI moyen global (0,651) et gagne tant que les courbes séparent les classes
  (0,938 et 0,887 en S1–S2) ; quand le signal fonctionnel est divisé par deux, FPCA + k-means
  gagne S3 (0,623) et la distance sur les dérivées seule gagne S4 (0,378).
- **L'ACP hybride (HFV) ne bat pas le produit de noyaux simple** : elle est derrière lui dans
  62 % à 78 % des tirages appariés selon le scénario, et à égalité (à 0,003 près) sur données réelles.
- **L'instabilité bootstrap (Fang & Wang) ne retrouve pas k** : le vrai nombre de classes est
  choisi en 1 point sur 441 de la grille pour Canadian Weather et 4 sur 441 pour Tecator.

## Méthodes comparées

- **Lignes de base** : distance $L^2$ entre courbes ($D_0$), entre dérivées ($D_1$), euclidienne
  sur les covariables standardisées ($D_s$).
- **A** : scores de l'ACP fonctionnelle (95 % de variance) concaténés à Z, puis k-means.
- **B** : distance pondérée
  $D_w(\alpha,\omega)=\sqrt{\omega\,[(1-\alpha)\tilde D_0^2+\alpha\tilde D_1^2]+(1-\omega)\tilde D_s^2}$, puis PAM.
- **C** : produit de noyaux gaussiens $K_f K_s$, distance induite
  $D_K=\sqrt{K_{ii}+K_{jj}-2K_{ij}}$, puis PAM.
- **HFV** : ACP hybride sur la covariance jointe
  $\begin{pmatrix}V_y & V_{yx}\\ V_{xy} & V_x\end{pmatrix}$, courbes reconstruites, puis $D_K$.

Règle de conduite : les hyperparamètres sont choisis par silhouette ; l'ARI (vérité terrain)
ne sert qu'à évaluer les partitions finales.

## Reproduire

R 4.x et les paquets CRAN `fda`, `fda.usc`, `cluster`, `mclust`, `fpc` (les données sont
fournies par ces paquets).

```bash
make setup && make pipeline   # trois jeux réels
make exp03                    # benchmark simulé (long)
make exp01                    # instabilité bootstrap (long)
make tables && make report    # tableaux LaTeX et mémoire
make figures && make check    # figures et chiffres du README (Python, uv, sans R)
```

## Limites

- k est fixé au vrai nombre de classes dans toutes les comparaisons de méthodes.
- Jeux réels de petite taille (35 stations pour Canadian Weather) ; une seule exécution par
  méthode, sans intervalle de rééchantillonnage.
- Sur Tecator, l'étiquette (taux de gras discrétisé) est chimiquement liée aux covariables
  (eau, protéines) ; sur Growth, les covariables sont calculées à partir de la courbe.
- Les conclusions simulées dépendent du générateur `Cas2_deriv`.
- Versions des paquets non figées (pas de `renv.lock`) ; `make setup` enregistre `sessionInfo()`.

Références et sources des données : [docs/biblio/README.md](docs/biblio/README.md).
