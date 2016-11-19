class ConvertUnitMixin(object):
    @property
    def convert_unit(self):
        boxes, pieces = divmod(self.units_in_stock, self.quantity_per_unit)
        # reduce(lambda rst, d: rst * 10 + d, (1, 2, 3))

        self._converted_units = (boxes, pieces)
        print(self._converted_units)
        return ','.join(map(str, self._converted_units))
        # return self._converted_units

    @convert_unit.setter
    def convert_unit(self, value):
        from ast import literal_eval
        r_tup = literal_eval(value)  # creates tuple from string 2,3
        print('-----saved----', r_tup)
        lambda_sum = lambda b, p: b * self.quantity_per_unit + p
        from functools import reduce
        # calc_stock_units = reduce(lambda_sum, r_tup)
        # self.units_in_stock = calc_stock_units
        if self._converted_units == r_tup:
            print("eq")
        elif self._converted_units < r_tup:
            print('more')
        else:
            print('less')
        self._converted_units = r_tup

from functools import reduce
class ToBoxMixin(object):
    @property
    def to_box(self):
        boxes,peices = divmod(self.quantity, self.product.quantity_per_unit)
        return '{},{}'.format(boxes, peices)

    @to_box.setter
    def to_box(self, value):
        #value '9,9'
        new_list = value.split(',')
        # print(value,' to_box mixin 000000000000', new_list)
        try:
            b = int(new_list[0])
        except ValueError:
            b = 0
        try:
            p = int(new_list[1])
        except IndexError:
            p = 0

        print('to_box setter Mixin b{} - p{}, value{}'.format(b,p, new_list))
        total_pieces = (b * self._multiplier) + p
        print('value:{} boxes:{}  pieces:{} total:{}' .format(value, b, p, total_pieces))

        # int_list = list(map(int, value.split(',', 1),))
        # print(int_list)
        # total_pieces = reduce((lambda x, y: x * multiplier + y), int_list)

        return total_pieces

    @property
    def to_pieces(self):
        # @to_box.setter
        # def to_box(self, value):
        # '2,9'   reduce((lambda x,y: x*10+y), s) => '33333333'
        # list(map(int, s.split(','))) = [2,9]
        # reduce((lambda x, y: x * 10 + y), intlist)  => 29

        # multiplier = self.product.quantity_per_unit
        # int_list = list(map(int, self.to_box.split(',')))
        # total_pieces = reduce((lambda x, y: x * multiplier + y), int_list)

        p, b = 0, 0
        new_list = self.to_box.split(',')
        try:
            b = int(new_list[0])
            p = int(new_list[1])
        except ValueError:
            pass
        except IndexError:
            pass
        total_pieces = b * self._multiplier + p

        return total_pieces

    def to_box_from_value(self, value, prod):
        if hasattr(self, 'product'):
            self._multiplier = self.product.quantity_per_unit
        else:
            from products.models import Product
            product = Product.objects.get(id=prod)
            self._multiplier = product.quantity_per_unit

        self.to_box = value
