from random import shuffle

def get_rnd_months(not_this, n = 3, rf=None):
    months = ["January", "February", "March", "May", "June", "July", "August", "September",
              "October", "November", "December"]
    if rf is not None:
        months = months[:rf]
    shuffle(months)
    if not_this in months[:n]:
        return months[n:2*n]
    return months[:n]

def too_close(ans, ins):
    per = 20*ans/100
    if ans-per <= ins <= ans+per:
        print "too close!"
        return True
    return False