# gjennomsnitt og standardavvik x og y
x_snitt = statistics.mean(x_verdier)
y_snitt = statistics.mean(y_verdier)

x_stdev = statistics.stdev(x_verdier)
y_stdev = statistics.stdev(y_verdier)

# Korrelasjon
cor = statistics.correlation(x_verdier, y_verdier)

# Kryssplott
kryss = sns.relplot(x = x_verdier,y = y_verdier)
kryss.fig.suptitle("Kryssplott av x og y", fontsize=14)
kryss.set_axis_labels("X", "Y")
plt.show()

print("Gjennomsnitt for x:", x_snitt)
print("Gjennomsnitt for y:", y_snitt)
print("Empirisk standardavvik for x:", x_stdev)
print("Empirisk standardavvik for y:", y_stdev)
print("Korrelasjon x og y:", cor)