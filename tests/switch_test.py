from mehr import switch, safe_switch

def test_normal_use():
    i = 4
    j = 0


    with switch(i) as (case, default, break_):
        if case(2):
            j = 1
        if case(4):
            j = 2
        if case(10):
            j = 5
            break_()
        if case(25):
            print(f"case 25")
            j = 12.5

    assert(j == 5)
