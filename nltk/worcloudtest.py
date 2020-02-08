import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
#https://amueller.github.io/word_cloud/auto_examples/a_new_hope.html
text = "square"

x, y = np.ogrid[:300, :300]

mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
mask = 255 * mask.astype(int)


wc = WordCloud(background_color="white", repeat=True, mask=mask)
wc.generate(text)

plt.axis("off")
plt.imshow(wc, interpolation="bilinear")
plt.show()