"""Just for initial dev period not an actual function of the program
"""

import sqlite3

with sqlite3.connect("focusflow.db") as con:
    cur = con.cursor()
    cur.execute("DELETE FROM task_info;") 
    con.commit()

print("All tasks deleted!")