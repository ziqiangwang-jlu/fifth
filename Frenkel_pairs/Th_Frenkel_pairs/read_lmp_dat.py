#! /public/home/ziqiangw/anaconda3/bin/python



class Read_data:
    def __init__(self, data):
        with open (data, 'r') as file:
            line = file.readline()
            line = file.readline()
            line = file.readline()
            tot_num = int(line.split()[0])
            self.tot_num = tot_num
            line = file.readline()
            atom_type = int(line.split()[0])
            self.tot_type = atom_type
            line = file.readline()
            line = file.readline()
            self.xlo, self.xhi = float(line.split()[0]), float(line.split()[1])
            line = file.readline()
            self.ylo, self.yhi = float(line.split()[0]), float(line.split()[1])
            line = file.readline()
            self.zlo, self.zhi = float(line.split()[0]), float(line.split()[1])
            line = file.readline()
            if len(line.split()) == 0:
                print('The box is orthogonal')
                #raise Exception("The triclinic configuration is excepted, but orthogonal is given")
            else:
                self.xy, self.xz, self.yz = float(line.split()[0]), float(line.split()[1]), float(line.split()[2])
                line = file.readline()
            for i in range(self.tot_type+5):
                line = file.readline()
            self.pos_dict = {}
            while True:
                line = file.readline()
                if len(line.split()) == 0:
                    break
                else:
                    ls = line.split()
                    self.pos_dict[int(ls[0])] = (int(ls[2]), float(ls[4]), float(ls[5]), float(ls[6]))

    def get_tot_num(self):
        return self.tot_num
    def get_tot_type(self):
        return self.tot_type
    def get_xlo(self):
        return self.xlo
    def get_xhi(self):
        return self.xhi
    def get_ylo(self):
        return self.ylo
    def get_yhi(self):
        return self.yhi
    def get_zhi(self):
        return self.zhi
    def get_zlo(self):
        return self.zlo
    def get_lx(self):
        lx = self.xhi-self.xlo
        return lx
    def get_ly(self):
        ly = self.yhi-self.ylo
        return ly
    def get_lz(self):
        lz = self.zhi-self.zlo
        return lz
    def get_tri_xy(self):
        return self.xy
    def get_tri_xz(self):
        return self.xz
    def get_tri_yz(self):
        return self.yz
    def get_type(self, id):
        return self.pos_dict[id][0]
    def get_position(self, id):
        return self.pos_dict[id][1:4]

if __name__ == '__main__':
    test = Read_data('perfect_relaxed.dat')
    print(test.get_tot_num())
    #print(test.get_tri_xz())
    print(test.get_position(109))
    print(test.get_xhi())
    print(test.get_tot_type())
    print(test.get_type(109))

