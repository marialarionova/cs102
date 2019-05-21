def entropy(img):
    freq = np.array([0 in range(256)])
    
    for row in img:
        for px in row:
            freq[px] += 1
            
    freq = freq / (len(img) * len(img[0]))
    ent = -np.sum([p * np.log2(p) for p in freq if p != 0])
    
    return ent
    
def rmse(img1, img2):
    return np.sqrt(np.sum(np.power(img1 - img2, 2)) / img1.shape[0] / img1.shape[1])
    
def psnr(img1, img2):
    rmse_val = rmse(img1, img2)
    
    if rmse_val == 0: return 100
    
    px__max = 255.0
    
    return 20 * np.log10(px__max / np.sqrt(rmse_val))
