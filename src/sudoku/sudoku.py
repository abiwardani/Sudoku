class Board:
    def __init__(self,state=None):
        template = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
        if state == None:
            self.map = template
        else:
            self.map = state
        
        tempprob = [[i for i in j] for j in template]
        for i in range(9):
            for j in range(9):
                tempprob[i][j] = []
        
        self.prob = tempprob
        
        self.gcount = 0
        
        self.possible = self.possibility(self.map)
        
        self.solution = 0
        
        return None
    
    def mprint(self,map=[]):
        if map == []:
            map = self.map
        
        for r in range(9):
            for c in range(9):
                print(map[r][c],end=" ")
                if c == 2 or c == 5:
                    print("|",end=" ")
            if r == 2 or r == 5:
                print("\n"+"_"*21)
            else:
                print("\n")
        return None
    
    def sq_check(self,n,k,map):
        r = (n//3)*3+1
        c = (n%3)*3+1
        u = [[map[i][j] for j in range(c-1,c+2)] for i in range(r-1,r+2)]
        for each in u:
            if k in each:
                return True
        return False

    def row_check(self,r,k,map):
        u = [map[r][i] for i in range(9)]
        if k in u:
            return True
        else:
            return False

    def col_check(self,c,k,map):
        u = [map[i][c] for i in range(9)]
        if k in u:
            return True
        else:
            return False
    
    def unfinished(self,map):
        for i in map:
            for j in i:
                if j == 0:
                    return True
        return False
        
    def possibility(self,map):
        self.prob_run(map)
        
        for i in self.prob:
            for j in i:
                if len(j) >= 1:
                    return True
        return False
    
    def prob_run(self,map):
        for r in range(9):
            for c in range(9):
                if map[r][c] != 0:
                    self.prob[r][c] = []
                else:
                    tempprob = ["" for x in range(9)]
                    ind = 0
                    n = (r//3)*3+(c//3)
                    for k in range(1,10):
                        if (self.row_check(r,k,map) == False and self.col_check(c,k,map) == False) and (self.sq_check(n,k,map) == False):
                            tempprob[ind] = k
                            ind += 1
                    self.prob[r][c] = [x for x in tempprob if x != ""]
        return None
    
    def block_column_interaction(self,map):
        for a in range(9):
            h = (a//3)*3+1
            v = (a%3)*3+1
            for k in range(1,10):
                countr = 0
                countc = 0
                for u in range(3):
                    if k in [map[u+h-1][i] for i in range(v-1,v+2)]:
                        countr += 1
                        rr = u+h-1
                    if k in [map[i][u+v-1] for i in range(h-1,h+2)]:
                        countc += 1
                        cc = u+v-1
                        
                if countr == 1:
                    for cr in range(9):
                        if cr not in range(v-1,v+2) and k in self.prob[rr][cr]:
                            self.gcount = 0
                            self.prob[rr][cr] = [x for x in self.prob[rr][cr] if x != k]
                if countc == 1:
                    for rc in range(9):
                        if rc not in range(h-1,h+2) and k in self.prob[rc][cc]:
                            self.gcount = 0
                            self.prob[rc][cc] = [x for x in self.prob[rc][cc] if x != k]
        
        return None
    
    def brute_force(self,case,temp_map=[]):
        if temp_map == []:
            temp_map = [[j for j in i] for i in self.map]
        
        keeper = [[j for j in i] for i in temp_map]
        
        self.prob_run(temp_map)
        
        if case == True and self.unfinished(temp_map) and self.solution == 0:
            self.gcount = 0
            self.solve(temp_map)
        
        if case == False and self.unfinished(temp_map) and self.solution == 0:
            for r in range(9):
                for c in range(9):
                    if temp_map[r][c] == 0:
                        for k in self.prob[r][c]:
                            if self.unfinished(temp_map) and self.solution == 0:
                                self.possible = self.possibility(temp_map)
                                
                                temp_map = [[j for j in i] for i in keeper]
                                temp_map[r][c] = k
                                case = True
                                self.brute_force(case,temp_map)
                            else:
                                return temp_map
                    if self.unfinished(temp_map) == False and self.solution != 0:
                        return temp_map
                if self.unfinished(temp_map) == False and self.solution != 0:
                    return temp_map
        
        return temp_map
        
    def solve(self,map=[]):
        
        if map == []:
            map = [[j for j in i] for i in self.map]
        
        self.gcount = 0
        
        self.prob_run(map)
        
        while self.unfinished(map) and self.possible and self.solution == 0:
            self.prob_run(map)
            
            self.possible = self.possibility(map)
            
            case = False
            
            for r in range(9):
                for c in range(9):
                    if len(self.prob[r][c]) == 1:
                        map[r][c] = self.prob[r][c][0]
                        case = True
                        self.prob_run(map)
                        
                    
            if case == False:
                for a in range(9):
                    kr = [0 for i in range(9)]
                    kc = [0 for i in range(9)]
                    ks = [0 for i in range(9)]
                    indr = 0
                    indc = 0
                    inds = 0
                    h = (a//3)*3+1
                    v = (a%3)*3+1
                    for b in range(9):
                        #unique_row
                        
                        r = a
                        
                        for k in self.prob[a][b]:
                            if k not in kr:
                                kr[indr] = k
                                indr += 1
                                count = 0
                                for c in range(9):
                                    if k in self.prob[r][c]:
                                        count += 1
                                        rp = r
                                        cp = c
                                if count == 1:
                                    map[rp][cp] = k
                                    case = True
                            if case: break
                        
                        #unique_col
                        
                        c = a
                        
                        for k in self.prob[b][a]:
                            if k not in kc:
                                kc[indc] = k
                                indc += 1
                                count = 0
                                for r in range(9):
                                    if k in self.prob[r][c]:
                                        count += 1
                                        rp = r
                                        cp = c
                                if count == 1:
                                    map[rp][cp] = k
                                    case = True
                            if case: break
                        
                        #unique_sq
                        
                        rn = b//3+h-1
                        cn = b%3+v-1
                        
                        for k in self.prob[rn][cn]:
                            if k not in ks:
                                ks[inds] = k
                                inds += 1
                                count = 0
                                for r in range(h-1,h+2):
                                    for c in range(v-1,v+2):
                                        if k in self.prob[r][c]:
                                            count += 1
                                            rp = r
                                            cp = c
                                if count == 1:
                                    map[rp][cp] = k
                                    case = True
                            if case: break
            
            if case == False and self.unfinished(map):
                self.gcount += 1
                self.block_column_interaction(map)
            else:
                self.gcount = 0
            
            if self.gcount >= 1:
                map = self.brute_force(False,map)
        
        if self.unfinished(map) == False:
            self.solution = [[j for j in i] for i in map]
            
            self.mprint(self.solution)
            
            exit()
            
            return True