from PIL import Image

imageObject = Image.open("./with_medicine.jpg")

doctors_name = imageObject.crop((10, 100, 1000, 500))
registration_number = imageObject.crop((1100, 150, 1900, 300))
email = imageObject.crop((1500, 410, 2150, 500))
doctors_sig = imageObject.crop((10, 2700, 1000, 3000))
stamp = imageObject.crop((1100, 2000, 1900, 2500))

prsp1 = imageObject.crop((100, 910, 1400, 1170))
prsp2 = imageObject.crop((100, 1170, 1400, 1410))
prsp3 = imageObject.crop((100, 1410, 1400, 1620))
prsp4 = imageObject.crop((100, 1620, 1400, 1830))
prsp5 = imageObject.crop((100, 1830, 1400, 2070))

dosage1 = imageObject.crop((1400, 910, 2100, 1170))
dosage2 = imageObject.crop((1400, 1170, 2100, 1410))
dosage3 = imageObject.crop((1400, 1410, 2100, 1620))
dosage4 = imageObject.crop((1400, 1620, 2100, 1830))
dosage5 = imageObject.crop((1400, 1830, 2100, 2070))

# doctors_name.show()
# registration_number.show()
# email.show()
# doctors_sig.show()
# stamp.show()

# prsp1.show()
# prsp2.show()
# prsp3.show()
# prsp4.show()
# prsp5.show()

dosage1.show()
dosage2.show()
dosage3.show()
dosage4.show()
dosage5.show()
