.. Origin_Server documentation master file, created by
   sphinx-quickstart on Wed Jan 12 13:05:31 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Origin_Server's documentation!
=========================================

**Author** *CABOS Matthieu*

**Date**  *2021/2022*

**Organization** *ICGM-CNRS*

______________________________________________________________________________________________________

These Scripts have been written to manage properly an Origin Server (See `Origin <https://ritme.com/software/origin/>`_)

It is adapted to the Origin ssh platform

(reading and treating **opt/Linux_FLEXnet_Server_ver_11.16.5.1/Licenses** and **/usr/local/flexlm/orglabdebug.log** wich are the Licence File and the Tokens Log file)

These scripts need a ssh session access into the origin server (with form origin.domain.fr)

These main scripts have been written to automate the DHCP Informations retrievment and Origin Server essentials informations.

The main project is made of the following files :

   * **Get_Origin_Info**
   * **Origin_API**
   * **Treat_tokens**
   * **Treat_log_v2**

The others file concern two pre-versions of the project. Each of them is associated to its API:

   * **Origin_Users_parallelisation_v2**
   * **Origin_Users_parallelisation_v2 associated API**
   * **Get_User_Info_From_IP_v2**
   * **Get_User_Info_From_IP_v2 associated API**

.. toctree::
   :maxdepth: 2

   Get_Origin_Info_v2.1
   Get_Origin_Info
   Origin_API
   Treat_tokens
   Treat_log_v2.1
   Origin_Users_parallelisation_v2
   Origin_Users_parallelisation_v2_API
   Get_User_Info_From_IP_v2
   Get_User_Info_From_IP_v2_API

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
