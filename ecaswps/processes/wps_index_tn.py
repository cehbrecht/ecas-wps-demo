import os
from pywps import Process, LiteralInput, ComplexOutput
from pywps import Format
from pywps.app.Common import Metadata


# ALLOWED_VALUES = {
#     'model':
#         'ACCESS1-0 ACCESS1-3 bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanCM4 '
#         'CanESM2 CCSM4 CESM1-BGC CESM1-CAM5 CESM1-WACCM CMCC-CM CMCC-CMS '
#         'CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 FIO-ESM GFDL-CM2p1 '
#         'GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H GISS-E2-H-CC GISS-E2-R '
#         'GISS-E2-R-CC HadCM3 HadGEM2-AO HadGEM2-CC HadGEM2-ES inmcm4 '
#         'IPSL-CM5A-LR IPSL-CM5A-MR IPSL-CM5B-LR MIROC4h MIROC5 MIROC-ESM '
#         'MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MRI-CGCM3 NorESM1-M NorESM1-ME'.split(),
#     'experiment':
#         'rcp45 rcp60 rcp8'.split(),
# }


class TropicalNights(Process):
    def __init__(self):
        inputs = [
            LiteralInput('dataset', 'Dataset',
                         data_type='string'),
            # LiteralInput('model', 'Model',
            #              default='HadGEM2-ES', data_type='string',
            #              allowed_values=ALLOWED_VALUES['model']),
            # LiteralInput('experiment', 'Experiment',
            #              default='rcp45', data_type='string',
            #              allowed_values=ALLOWED_VALUES['experiment']),
            # LiteralInput('start_year', 'Start Year',
            #              default='2010', data_type='integer'),
            # LiteralInput('end_year', 'End Year',
            #              default='2020', data_type='integer'),
        ]
        outputs = [
            ComplexOutput('output', 'Output plot',
                          abstract='Map of Trophical Nights',
                          as_reference=True,
                          supported_formats=[Format('image/png')])
        ]

        super(TropicalNights, self).__init__(
            self._handler,
            identifier='tropical_nights',
            version='1.0',
            title='Tropical Nights',
            abstract='Computes the Tropical Nights index: '
            'starting from the daily minimum temperature (1980-1990) TN, '
            'the Tropical Nights index is the number of days where TN > T '
            '(T is  a reference temperature, e.g. 20 degree celsius)',
            profile='',
            metadata=[
                Metadata('ECASLab', 'https://ecaslab.dkrz.de/home.html'),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from ecaswps.toolbox import tropical_nights
        response.update_status('Calculting TN ...', 0)
        # output in workdir
        output_filename = os.path.join(self.workdir, 'output.png')
        # start TN
        tropical_nights(
            dataset=request.inputs['dataset'][0].data,
            output=output_filename)
        # store result
        response.outputs['output'].file = output_filename
        # done
        response.update_status('TN done', 100)
        return response
