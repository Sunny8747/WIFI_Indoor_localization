BW = imbinarize(rgb2gray(imread('Bf4.bmp')));
X = size(BW,1);
Y = size(BW,2);
for x = 1:X
    for y = 1:Y
        if BW(x,y) == 0
            BW(x,y) = 1;
        else
            BW(x,y) = 0;
        end
    end
end
imshow(BW);
imsave;
