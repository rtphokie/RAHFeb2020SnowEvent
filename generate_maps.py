import unittest
from mapping import draw_wfo_dma_map, _drawmap, plot_shapes, get_snowfall_categories, plot_forecasts, NWSLegend, extract_range
from pprint import pprint

class MyTestCase(unittest.TestCase):
    def dtest_DMA_map(self):
        # NWScolormap(NWSLegend)
        draw_wfo_dma_map(res='i', DMAs=['RALEIGH-DURHAM'], WFOs=['GSP', 'RAH', 'AKQ', 'MHX', 'RNK', 'ILM'])

    def test_forecasts(self):
        resultsdir = 'data/shapefiles/20200220NCSnowResults'
        forecastdir = 'data/shapefiles/20200220NCSnowForecasts'
        resultsfile = '20200220NCSnowResults'
        NWS_categories = get_snowfall_categories(resultsdir, resultsfile)
        ax, fig, m = _drawmap('c', drawstates=True, drawcountries=True, drawcoastlines=True)
        steps = [-0.1, 1.0, 2.0, 3.0, 5.0]

        for i in range(1, len(steps)):
            bucket_top = steps[i]
            bucket_bottom = steps[i-1]+0.1
            print(f"{bucket_bottom}-{bucket_top}")

            ax, fig, m = _drawmap('l', drawstates=True, drawcountries=True, drawcoastlines=True)
            fig.text(0.5, 0.92, f"forecasts of {bucket_bottom}-{bucket_top} inches", horizontalalignment='center')
            for category, bounds in NWS_categories.items():
                if bounds['lower'] >= bucket_bottom and bounds['upper'] <= bucket_top:
                    print(f" NWS: {category}")
                    plot_shapes(ax, m, resultsdir, resultsfile, 'Name', category, {},
                                linewidths=0.0, facecolor='blue', alpha=.6, colorbylistposition=False,
                                labelcentroid=False)
            for forecast in ['forecastA','forecastB', 'forecastC', 'forecastD']:
                # loop through shapefiles for 4 broadcast forecasts
                m.readshapefile(f'{forecastdir}/{forecast}', forecast, ax=ax, drawbounds=False)
                for info, shape in zip(m.__dict__[f"{forecast}_info"], m.__dict__[forecast]):
                    lowerbound, upperbound = extract_range(info['Name'])
                    if (upperbound <= bucket_top and upperbound >= bucket_bottom) or \
                       (lowerbound >= bucket_bottom and lowerbound <= bucket_top):
                        # forecasted range falls anywhere in this bucket
                        print(f"  +{forecast}: {info['Name']}")
                        plot_shapes(ax, m, forecastdir, forecast, 'Name', info['Name'], {},
                                    linewidths=0.0, facecolor='grey', alpha=0.25, colorbylistposition=False,
                                    labelcentroid=False)
                    else:
                        print(f"   {forecast}: {info['Name']}")
            # outline DMA
            plot_shapes(ax, m, 'data/shapefiles/dma_2008', 'DMAs', 'NAME', ['RALEIGH-DURHAM'], {},
                        linewidths=2.0, colorbylistposition=False, labelcentroid=False)
            fig.savefig(f'forecasts_{bucket_top}.png')
            fig.show()
            print('-' * 20)

        return


        for x in range(1,6):
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
