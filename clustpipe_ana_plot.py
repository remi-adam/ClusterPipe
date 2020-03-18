"""
This file contains plotting tools for the CTA analysis.

"""

#==================================================
# Requested imports
#==================================================

import os
import astropy.units as u
import gammalib

from ClusterPipe.Tools import plotting
from clustpipe_sim_plot import skymap_quicklook


#==================================================
# Plot the observing properties
#==================================================

def observing_setup(cpipe):
    """
    Function runing the observing properties
    
    Parameters
    ----------
    - cpipe (ClusterPipe object): a cluster pipe object 
    associated to the analysis

    Outputs
    --------
    - plots
    """

    plotting.show_pointings(cpipe.output_dir+'/Ana_ObsDef.xml',
                            cpipe.output_dir+'/Ana_ObsPointing.png')

    plotting.show_obsdef(cpipe.output_dir+'/Ana_ObsDef.xml', cpipe.cluster.coord,
                         cpipe.output_dir+'/Ana_ObsDef.png')

    plotting.show_irf(cpipe.obs_setup.caldb, cpipe.obs_setup.irf, cpipe.output_dir+'/Ana_ObsIRF')

    
#==================================================
# Plot the observing properties
#==================================================

def events_quicklook(cpipe, obsID,
                     smoothing_FWHM=0.1*u.deg):
    """
    Function runing the event file analysis
    
    Parameters
    ----------
    - cpipe (ClusterPipe object): a cluster pipe object 
    associated to the analysis
    - obsID (list): the list of obsID to look at
    - smoothing_fwhm (quantity): the FWHM value used for smoothing the maps

    Outputs
    --------
    - plots
    """
    
    for iobs in obsID:
        if os.path.exists(cpipe.output_dir+'/Ana_SelectedEvents'+
                          cpipe.obs_setup.select_obs(iobs).obsid[0]+'.fits'):
            plotting.events_quicklook(cpipe.output_dir+'/Ana_SelectedEvents'+
                                      cpipe.obs_setup.select_obs(iobs).obsid[0]+'.fits',
                                      cpipe.output_dir+'/Ana_SelectedEvents'+
                                      cpipe.obs_setup.select_obs(iobs).obsid[0]+'.png')
            
            skymap_quicklook(cpipe.output_dir+'/Ana_Skymap'+cpipe.obs_setup.select_obs(iobs).obsid[0],
                             cpipe.output_dir+'/Ana_SelectedEvents'+
                             cpipe.obs_setup.select_obs(iobs).obsid[0]+'.fits',
                             cpipe.obs_setup.select_obs(iobs), cpipe.compact_source, cpipe.cluster,
                             map_reso=cpipe.map_reso, smoothing_FWHM=smoothing_FWHM, bkgsubtract='NONE',
                             silent=True, MapCenteredOnTarget=True)


#==================================================
# Plot the maps
#==================================================

def combined_maps(cpipe,
                  obsID,
                  smoothing_FWHM=0.1*u.deg):
    """
    Function running the map plotting
    
    Parameters
    ----------
    - cpipe (ClusterPipe object): a cluster pipe object 
    associated to the analysis
    - obsID (list): the list of obsID used for analysis
    - smoothing_fwhm (quantity): the FWHM value used for smoothing the maps

    Outputs
    --------
    - plots
    """

    #----- Collect the point source list
    ps_name  = []
    ps_ra    = []
    ps_dec   = []
    for i in range(len(cpipe.compact_source.name)):
        ps_name.append(cpipe.compact_source.name[i])
        ps_ra.append(cpipe.compact_source.spatial[i]['param']['RA']['value'].to_value('deg'))
        ps_dec.append(cpipe.compact_source.spatial[i]['param']['DEC']['value'].to_value('deg'))

    #----- Collect the pointing list
    ptg_name  = []
    ptg_ra    = []
    ptg_dec   = []
    for i in range(len(cpipe.obs_setup.name)):
        if cpipe.obs_setup.obsid[i] in obsID:
            ptg_name.append(cpipe.obs_setup.name[i])
            ptg_ra.append(cpipe.obs_setup.coord[i].icrs.ra.to_value('deg'))
            ptg_dec.append(cpipe.obs_setup.coord[i].icrs.dec.to_value('deg'))

    #========== Show the combined skymap
    plotting.show_map(cpipe.output_dir+'/Ana_SkymapTot.fits',
                      cpipe.output_dir+'/Ana_SkymapTot.pdf',
                      smoothing_FWHM=smoothing_FWHM,
                      cluster_ra=cpipe.cluster.coord.icrs.ra.to_value('deg'),
                      cluster_dec=cpipe.cluster.coord.icrs.dec.to_value('deg'),
                      cluster_t500=cpipe.cluster.theta500.to_value('deg'),
                      cluster_name=cpipe.cluster.name,
                      ps_name=ps_name,
                      ps_ra=ps_ra,
                      ps_dec=ps_dec,
                      ptg_ra=ptg_ra,
                      ptg_dec=ptg_dec,
                      #PSF=PSF_tot,
                      bartitle='Counts',
                      rangevalue=[None, None],
                      logscale=True,
                      significance=False,
                      cmap='magma')

    #========== Show the combined total residuals
    for alg in ['SIGNIFICANCE', 'SUB', 'SUBDIV']:
        if alg == 'SIGNIFICANCE':
            is_significance = True
            btitle = 'Significance'
            mrange = [-3, None]
        elif alg == 'SUB':
            is_significance = False
            btitle = 'Data-Model'
            mrange = [None, None]
        elif alg == 'SUBDIV':
            is_significance = False
            btitle = '(Data-Model)/Model'
            mrange = [None, None]
            
        plotting.show_map(cpipe.output_dir+'/Ana_ResmapTot_'+alg+'.fits',
                          cpipe.output_dir+'/Ana_ResmapTot_'+alg+'.pdf',
                          smoothing_FWHM=smoothing_FWHM,
                          cluster_ra=cpipe.cluster.coord.icrs.ra.to_value('deg'),
                          cluster_dec=cpipe.cluster.coord.icrs.dec.to_value('deg'),
                          cluster_t500=cpipe.cluster.theta500.to_value('deg'),
                          cluster_name=cpipe.cluster.name,
                          ps_name=ps_name,
                          ps_ra=ps_ra,
                          ps_dec=ps_dec,
                          ptg_ra=ptg_ra,
                          ptg_dec=ptg_dec,
                          #PSF=PSF_tot,
                          bartitle=btitle,
                          rangevalue=mrange,
                          logscale=False,
                          significance=is_significance,
                          cmap='magma')
        
        plotting.show_map(cpipe.output_dir+'/Ana_ResmapCluster_'+alg+'.fits',
                          cpipe.output_dir+'/Ana_ResmapCluster_'+alg+'.pdf',
                          smoothing_FWHM=smoothing_FWHM,
                          cluster_ra=cpipe.cluster.coord.icrs.ra.to_value('deg'),
                          cluster_dec=cpipe.cluster.coord.icrs.dec.to_value('deg'),
                          cluster_t500=cpipe.cluster.theta500.to_value('deg'),
                          cluster_name=cpipe.cluster.name,
                          ps_name=ps_name,
                          ps_ra=ps_ra,
                          ps_dec=ps_dec,
                          ptg_ra=ptg_ra,
                          ptg_dec=ptg_dec,
                          #PSF=PSF_tot,
                          bartitle=btitle,
                          rangevalue=mrange,
                          logscale=False,
                          significance=is_significance,
                          cmap='magma')
        
#==================================================
# Spectrum
#==================================================

def spectrum(cpipe):
    """
    Function running the spectrum plots
    
    Parameters
    ----------
    - cpipe (ClusterPipe object): a cluster pipe object 
    associated to the analysis

    Outputs
    --------
    - plots
    """

    #========== Flux for each source
    models = gammalib.GModels(cpipe.output_dir+'/Ana_Model_Output.xml')

    for isource in range(len(models)):
        srcname = models[isource].name()
        specfile = cpipe.output_dir+'/Ana_Spectrum_'+srcname+'.fits'
        outfile  = cpipe.output_dir+'/Ana_Spectrum_'+srcname+'.pdf'
        butfile  = cpipe.output_dir+'/Ana_Spectrum_Buterfly_'+srcname+'.txt'
        butexist = os.path.isfile(butfile)
        if butexist:
            plotting.show_spectrum(specfile, outfile, butfile=butfile)
        else:
            plotting.show_spectrum(specfile, outfile)

    #========== Residual counts in ROI
    plotting.show_spectrum_residual(cpipe.output_dir+'/Ana_Spectrum_Residual.fits',
                                    cpipe.output_dir+'/Ana_Spectrum_Residual.pdf')
