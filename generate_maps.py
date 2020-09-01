import unittest
from mapping import draw_wfo_dma_map, _drawmap, plot_shapes, get_snowfall_categories, plot_forecasts, NWSLegend, extract_range
from pprint import pprint

class MyTestCase(unittest.TestCase):
    def test_DMA_map(self):
        # NWScolormap(NWSLegend)
        draw_wfo_dma_map(res='i', DMAs=['RALEIGH-DURHAM'], WFOs=['GSP', 'RAH', 'AKQ', 'MHX', 'RNK', 'ILM'])

    def test_forecasts(self):
        resultsdir = 'data/shapefiles/20200220NCSnowResults'
        forecastdir = 'data/shapefiles/20200220NCSnowForecasts'
        resultsfile = '20200220NCSnowResults'
        categories = get_snowfall_categories(resultsdir, resultsfile)

        for category, bounds in categories.items():
        # category=''
        # if True:
            print(f"NWS {category}")
            ax, fig, m = _drawmap('i', drawstates=True, drawcountries=True, drawcoastlines=True)
            fig.text(0.5, 0.92, f"forecasts of {category} inches", horizontalalignment='center')

            # plot
            m.readshapefile(f'{resultsdir}/{resultsfile}', resultsfile, ax=ax, drawbounds=False)
            plot_shapes(ax, m, resultsdir, resultsfile, 'Name', category, {},
                        linewidths=0.0, facecolor=NWSLegend[category], alpha=1, colorbylistposition=False, labelcentroid=False)

            # plot the 4 forecasts for that depth
            for forecast in ['forecastA','forecastB', 'forecastC', 'forecastD']:
                m.readshapefile(f'{forecastdir}/{forecast}', forecast, ax=ax, drawbounds=False)
                for info, shape in zip(m.__dict__[f"{forecast}_info"], m.__dict__[forecast]):
                    lowerbound, upperbound = extract_range(info['Name'])
                    if lowerbound <= bounds ['upper'] or upperbound >= bounds ['lower']:
                        plot_shapes(ax, m, forecastdir, forecast, 'Name', category, {},
                                    linewidths=0.0, facecolor='grey', alpha=0.25, colorbylistposition=False,
                                    labelcentroid=False)
                        print(f"+{forecast} {info['Name']:6} {lowerbound:4.1f} - {upperbound:4.1f}")
                    else:
                        print(f" {forecast} {info['Name']:6} {lowerbound:4.1f} - {upperbound:4.1f}")

            fig.savefig(f'forecasts_up_to{category}.png')
            fig.show()
            print('-'*20)





if __name__ == '__main__':
    unittest.main()
