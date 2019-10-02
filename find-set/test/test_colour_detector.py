import unittest
from function.colour_detector import transform_point, identify
from os import listdir
from os.path import isfile, join


class ColourDetector(unittest.TestCase):

    def test_transform_point(self):
        self.assertEqual(transform_point(point(0, 0), 10, 10), (0, 0))
        self.assertEqual(transform_point(point(1, 1), 10, 10), (10, 10))
        self.assertEqual(transform_point(point(0.5, 0.1), 10, 10), (5, 1))

    def test_identify(self):
        for file_name in listdir('test/images'):
            file = join('test/images', file_name)
            if isfile(file):
                expected_colour = file_name[1]
                with self.subTest(msg="Checking if image is colour", image=file, colour=expected_colour):
                    with open(file, 'rb') as image_file:
                        image_data = image_file.read()
                        bounding_box = create_bounding_box((0, 0, 1, 1))
                        self.assertEqual(identify(image_data, bounding_box), expected_colour)

    def test_identify_all_red(self):
        coords_list = [
            (0.5308570265769958, 0.36052098870277405, 0.6039609909057617, 0.6050900220870972),
            (0.23275800049304962, 0.3991140127182007, 0.3132689893245697, 0.6381869912147522),
            (0.3505550026893616, 0.09201960265636444, 0.42208099365234375, 0.3177050054073334),
            (0.32738301157951355, 0.6436910033226013, 0.4071210026741028, 0.909296989440918),
            (0.6242330074310303, 0.374891996383667, 0.6908389925956726, 0.6057959794998169),
            (0.4380260109901428, 0.0916299968957901, 0.5144810080528259, 0.32589098811149597),
            (0.43539300560951233, 0.3546600043773651, 0.5067330002784729, 0.6053599715232849),
            (0.6260700225830078, 0.655273973941803, 0.698714017868042, 0.9106829762458801),
            (0.25877299904823303, 0.11431799829006195, 0.32862600684165955, 0.3121950030326843),
            (0.5421950221061707, 0.08898740261793137, 0.6152060031890869, 0.31870898604393005),
            (0.22143299877643585, 0.6914160251617432, 0.302278995513916, 0.9437620043754578),
            (0.33400699496269226, 0.3575359880924225, 0.41206100583076477, 0.609607994556427),
            (0.4285149872303009, 0.6344599723815918, 0.5079339742660522, 0.9025819897651672),
            (0.6445749998092651, 0.1073089987039566, 0.7161980271339417, 0.33254799246788025),
            (0.5279780030250549, 0.6460949778556824, 0.6029549837112427, 0.9000980257987976),
        ]
        self.full_image_test('test/images/full/all_red.jpg', coords_list, "R")

    def test_identify_all_green(self):
        coords_list = [
            (0.5722169876098633, 0.04028109833598137, 0.6499000191688538, 0.29730600118637085),
            (0.2489120066165924, 0.05548449978232384, 0.32580500841140747, 0.3047949969768524),
            (0.35637998580932617, 0.04265400022268295, 0.4353939890861511, 0.2989250123500824),
            (0.687388002872467, 0.3352090120315552, 0.7614129781723022, 0.5951930284500122),
            (0.2493550032377243, 0.3424049913883209, 0.32817599177360535, 0.6162760257720947),
            (0.46764400601387024, 0.046290699392557144, 0.5488790273666382, 0.28580498695373535),
            (0.23607000708580017, 0.7118189930915833, 0.3234669864177704, 0.9862390160560608),
            (0.6803709864616394, 0.0667743980884552, 0.7540069818496704, 0.3033210039138794),
            (0.6803709864616394, 0.0667743980884552, 0.7540069818496704, 0.3033210039138794),
            (0.6021689772605896, 0.6730129718780518, 0.6771119832992554, 0.9486510157585144),
            (0.35841700434684753, 0.6894569993019104, 0.4408310055732727, 0.9586179852485657),
            (0.7038829922676086, 0.6816830039024353, 0.7840350270271301, 0.9474160075187683),
            (0.4624199867248535, 0.34258899092674255, 0.5467420220375061, 0.6010630130767822),
            (0.35623699426651, 0.3415890038013458, 0.4371969997882843, 0.6056089997291565),
            (0.4809879958629608, 0.6829040050506592, 0.5630729794502258, 0.9538040161132812),
            (0.5743759870529175, 0.32729798555374146, 0.6523659825325012, 0.5936579704284668)
        ]
        self.full_image_test('test/images/full/all_green.jpg', coords_list, "G")

    def test_identify_all_blue(self):
        coords_list = [
            (0.5572329759597778, 0.548147976398468, 0.6167600154876709, 0.7547850012779236),
            (0.5603209733963013, 0.3127239942550659, 0.6207460165023804, 0.5157070159912109),
            (0.6418399810791016, 0.3275650143623352, 0.7009919881820679, 0.5269209742546082),
            (0.3253050148487091, 0.05740490183234215, 0.3863779902458191, 0.2728630006313324),
            (0.4804379940032959, 0.543196976184845, 0.5362520217895508, 0.7399929761886597),
            (0.481126993894577, 0.31134098768234253, 0.5424060225486755, 0.5164459943771362),
            (0.4842909872531891, 0.07100749760866165, 0.5487030148506165, 0.277785986661911),
            (0.40680399537086487, 0.3151569962501526, 0.4639259874820709, 0.5094730257987976),
            (0.3260360062122345, 0.5373619794845581, 0.3868750035762787, 0.7342810034751892),
            (0.6463750004768372, 0.07891249656677246, 0.7125070095062256, 0.2899869978427887),
            (0.6363109946250916, 0.556850016117096, 0.6948689818382263, 0.7602739930152893),
            (0.405458003282547, 0.5374690294265747, 0.4614669978618622, 0.7384520173072815),
            (0.5671769976615906, 0.058107901364564896, 0.6255549788475037, 0.2947160005569458),
            (0.4047119915485382, 0.06543900072574615, 0.4666230082511902, 0.2743239998817444),
            (0.3247610032558441, 0.2966260015964508, 0.3904139995574951, 0.5115169882774353)
        ]
        self.full_image_test('test/images/full/all_blue.jpg', coords_list, "B")

    def full_image_test(self, image_name, coords_list, expected):
        bounding_boxes = [create_bounding_box(coords) for coords in coords_list]
        with open(image_name,  'rb') as image_file:
            image_data = image_file.read()
            for bounding_box in bounding_boxes:
                with self.subTest(bounding_box=bounding_box):
                    self.assertEqual(identify(image_data, bounding_box), expected)


def create_bounding_box(coords):
    return {
        'top_left': point(coords[1], coords[0]),
        'bottom_right': point(coords[3], coords[2]),
    }


def point(x, y):
    return {'x': x, 'y': y}


if __name__ == '__main__':
    unittest.main()
