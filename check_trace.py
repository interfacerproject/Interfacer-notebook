events = [
  {
    "ts": "2022-11-24T12:59:51.431034+00:00",
    "event_id": "062AKE8VMP4WJF6750DWQKFD1M",
    "action": "raise",
    "res_name": "soap",
    "res": "062AKE8VNDSK7Q0858QWWJ9RVM"
  },
  {
    "ts": "2022-11-24T12:59:51.650138+00:00",
    "event_id": "062AKE8WB5HDJE6HQMM64FFKJ4",
    "action": "raise",
    "res_name": "water",
    "res": "062AKE8WBHCEJWA61CRSXV3ZZC"
  },
  {
    "ts": "2022-11-24T12:59:51.829003+00:00",
    "event_id": "062AKE8WZHY8M32K5VHDPT6PDR",
    "action": "raise",
    "res_name": "cotton",
    "res": "062AKE8X08TNWYEZ47HJ2S1D2G"
  },
  {
    "ts": "2022-11-24T12:59:52.519880+00:00",
    "event_id": "062AKE8ZQ5A310PQ4T26E1Z4JW",
    "action": "consume",
    "res_name": "cotton",
    "res": "062AKE8X08TNWYEZ47HJ2S1D2G"
  },
  {
    "ts": "2022-11-24T12:59:52.519880+00:00",
    "event_id": "062AKE8XTC9QY4AJG4CQCSKXN4",
    "action": "Sew gown process",
    "res_name": "cotton",
    "res": "062AKE8X08TNWYEZ47HJ2S1D2G"
  },
  {
    "ts": "2022-11-24T12:59:52.684062+00:00",
    "event_id": "062AKE90DMVE2YXXG2G3F66S60",
    "action": "produce",
    "res_name": "gown",
    "res": "062AKE90E02WYJX5PR026X5MXM"
  },
  {
    "ts": "2022-11-24T12:59:52.878014+00:00",
    "event_id": "062AKE914D8PD688C0GGE8QH1M",
    "action": "transfer-custody",
    "res_name": "gown",
    "res": "062AKE9151GXYPRNW3GY6E5EP8"
  },
  {
    "ts": "2022-11-24T12:59:53.055176+00:00",
    "event_id": "062AKE91SXHP6JNWW1QNCXAAEW",
    "action": "work",
    "res_name": "gown",
    "res": "062AKE9151GXYPRNW3GY6E5EP8"
  },
  {
    "ts": "2022-11-24T12:59:53.198824+00:00",
    "event_id": "062AKE92CK2KWKWWYH0WPR7P2R",
    "action": "accept",
    "res_name": "gown",
    "res": "062AKE9151GXYPRNW3GY6E5EP8"
  },
  {
    "ts": "2022-11-24T12:59:53.198824+00:00",
    "event_id": "062AKE8YD2219BA5MDS2G7NGRG",
    "action": "Use gown process",
    "res_name": "gown",
    "res": "062AKE9151GXYPRNW3GY6E5EP8"
  },
  {
    "ts": "2022-11-24T12:59:53.368625+00:00",
    "event_id": "062AKE9315RKDFRC6YZ21A2XZG",
    "action": "modify",
    "res_name": "gown",
    "res": "062AKE9151GXYPRNW3GY6E5EP8"
  },
  {
    "ts": "2022-11-24T12:59:53.549441+00:00",
    "event_id": "062AKE93R902TAR8VTX92QGTW8",
    "action": "transfer-custody",
    "res_name": "gown",
    "res": "062AKE93SPWNBRYE9E47A9ZGG4"
  },
  {
    "ts": "2022-11-24T12:59:53.733246+00:00",
    "event_id": "062AKE94EBKCCY6YWVYCD6HNDW",
    "action": "accept",
    "res_name": "gown",
    "res": "062AKE93SPWNBRYE9E47A9ZGG4"
  },
  {
    "ts": "2022-11-24T12:59:53.902511+00:00",
    "event_id": "062AKE954XE4D36KYVB7V35SXW",
    "action": "consume",
    "res_name": "water",
    "res": "062AKE8WBHCEJWA61CRSXV3ZZC"
  },
  {
    "ts": "2022-11-24T12:59:54.076295+00:00",
    "event_id": "062AKE95TZEMVDK4V2KC83QC1G",
    "action": "consume",
    "res_name": "soap",
    "res": "062AKE8VNDSK7Q0858QWWJ9RVM"
  },
  {
    "ts": "2022-11-24T12:59:54.076295+00:00",
    "event_id": "062AKE8Z16MM9JSS8KXNSQCGGC",
    "action": "Clean gown process",
    "res_name": "soap",
    "res": "062AKE8VNDSK7Q0858QWWJ9RVM"
  },
  {
    "ts": "2022-11-24T12:59:54.248811+00:00",
    "event_id": "062AKE96HC545CKMNP087AVDC0",
    "action": "modify",
    "res_name": "gown",
    "res": "062AKE93SPWNBRYE9E47A9ZGG4"
  }
]
trace = {
    "data": {
        "economicResource": {
            "trace": [
                {
                    "__typename": "EconomicResource",
                    "accountingQuantity": {
                        "hasNumericalValue": "0",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    },
                    "classifiedAs": None,
                    "custodian": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "id": "062AKE93SPWNBRYE9E47A9ZGG4",
                    "name": "gown",
                    "note": None,
                    "onhandQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    },
                    "primaryAccountable": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "transferCustody"
                    },
                    "id": "062AKE93R902TAR8VTX92QGTW8",
                    "provider": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                            "name": "User One"
                        },
                        "id": "062AKE9151GXYPRNW3GY6E5EP8",
                        "name": "gown",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                            "name": "User One"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    }
                },
                {
                    "__typename": "EconomicResource",
                    "accountingQuantity": {
                        "hasNumericalValue": "0",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    },
                    "classifiedAs": None,
                    "custodian": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "id": "062AKE9151GXYPRNW3GY6E5EP8",
                    "name": "gown",
                    "note": None,
                    "onhandQuantity": {
                        "hasNumericalValue": "0",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    },
                    "primaryAccountable": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "modify"
                    },
                    "id": "062AKE9315RKDFRC6YZ21A2XZG",
                    "provider": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "receiver": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                            "name": "User One"
                        },
                        "id": "062AKE9151GXYPRNW3GY6E5EP8",
                        "name": "gown",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                            "name": "User One"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    }
                },
                {
                    "__typename": "Process",
                    "id": "062AKE8YD2219BA5MDS2G7NGRG",
                    "name": "Use gown process",
                    "note": "Use gown process performed by User One"
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "accept"
                    },
                    "id": "062AKE92CK2KWKWWYH0WPR7P2R",
                    "provider": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "receiver": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                            "name": "User One"
                        },
                        "id": "062AKE9151GXYPRNW3GY6E5EP8",
                        "name": "gown",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                            "name": "User One"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    }
                },
                {
                    "__typename": "EconomicResource",
                    "accountingQuantity": {
                        "hasNumericalValue": "0",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    },
                    "classifiedAs": None,
                    "custodian": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "id": "062AKE9151GXYPRNW3GY6E5EP8",
                    "name": "gown",
                    "note": None,
                    "onhandQuantity": {
                        "hasNumericalValue": "0",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    },
                    "primaryAccountable": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "transferCustody"
                    },
                    "id": "062AKE914D8PD688C0GGE8QH1M",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "1",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE90E02WYJX5PR026X5MXM",
                        "name": "gown",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    }
                },
                {
                    "__typename": "EconomicResource",
                    "accountingQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    },
                    "classifiedAs": None,
                    "custodian": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "id": "062AKE90E02WYJX5PR026X5MXM",
                    "name": "gown",
                    "note": None,
                    "onhandQuantity": {
                        "hasNumericalValue": "0",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    },
                    "primaryAccountable": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "produce"
                    },
                    "id": "062AKE90DMVE2YXXG2G3F66S60",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": {
                        "id": "0629XVVS5XKGFQP0KSHV6K4V18",
                        "name": "gown",
                        "note": "Specification for gowns"
                    },
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "1",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE90E02WYJX5PR026X5MXM",
                        "name": "gown",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    }
                },
                {
                    "__typename": "Process",
                    "id": "062AKE8XTC9QY4AJG4CQCSKXN4",
                    "name": "Sew gown process",
                    "note": "Sew gown process performed by User One"
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "consume"
                    },
                    "id": "062AKE8ZQ5A310PQ4T26E1Z4JW",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "10",
                            "hasUnit": {
                                "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                                "label": "kg",
                                "symbol": "om2:kilogram"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE8X08TNWYEZ47HJ2S1D2G",
                        "name": "cotton",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "10",
                            "hasUnit": {
                                "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                                "label": "kg",
                                "symbol": "om2:kilogram"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "10",
                        "hasUnit": {
                            "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                            "label": "kg",
                            "symbol": "om2:kilogram"
                        }
                    }
                },
                {
                    "__typename": "EconomicResource",
                    "accountingQuantity": {
                        "hasNumericalValue": "10",
                        "hasUnit": {
                            "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                            "label": "kg",
                            "symbol": "om2:kilogram"
                        }
                    },
                    "classifiedAs": None,
                    "custodian": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "id": "062AKE8X08TNWYEZ47HJ2S1D2G",
                    "name": "cotton",
                    "note": None,
                    "onhandQuantity": {
                        "hasNumericalValue": "10",
                        "hasUnit": {
                            "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                            "label": "kg",
                            "symbol": "om2:kilogram"
                        }
                    },
                    "primaryAccountable": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "raise"
                    },
                    "id": "062AKE8WZHY8M32K5VHDPT6PDR",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": {
                        "id": "0629XVVRKH9PNAW9NG6GGT631W",
                        "name": "cotton",
                        "note": "Specification for cotton to be used to sew the gowns"
                    },
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "10",
                            "hasUnit": {
                                "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                                "label": "kg",
                                "symbol": "om2:kilogram"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE8X08TNWYEZ47HJ2S1D2G",
                        "name": "cotton",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "10",
                            "hasUnit": {
                                "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                                "label": "kg",
                                "symbol": "om2:kilogram"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "20",
                        "hasUnit": {
                            "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                            "label": "kg",
                            "symbol": "om2:kilogram"
                        }
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "work"
                    },
                    "id": "062AKE91SXHP6JNWW1QNCXAAEW",
                    "provider": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "receiver": {
                        "id": "0629XVVJV2B9ZPEEG3V73ER2HG",
                        "name": "User One"
                    },
                    "resourceConformsTo": {
                        "id": "0629XVVSP7EB24Z6AREFEJ4QZ8",
                        "name": "surgical_operation",
                        "note": "Specification for surgical operations"
                    },
                    "resourceInventoriedAs": None,
                    "resourceQuantity": None
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "modify"
                    },
                    "id": "062AKE96HC545CKMNP087AVDC0",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE93SPWNBRYE9E47A9ZGG4",
                        "name": "gown",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "1",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    }
                },
                {
                    "__typename": "Process",
                    "id": "062AKE8Z16MM9JSS8KXNSQCGGC",
                    "name": "Clean gown process",
                    "note": "Clean gown process performed by User Two"
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "accept"
                    },
                    "id": "062AKE94EBKCCY6YWVYCD6HNDW",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "0",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE93SPWNBRYE9E47A9ZGG4",
                        "name": "gown",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "1",
                            "hasUnit": {
                                "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                                "label": "u_piece",
                                "symbol": "om2:one"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "1",
                        "hasUnit": {
                            "id": "0629XVVNA5SYG0F9AVGZNSBJA0",
                            "label": "u_piece",
                            "symbol": "om2:one"
                        }
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "consume"
                    },
                    "id": "062AKE954XE4D36KYVB7V35SXW",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "25",
                            "hasUnit": {
                                "id": "0629XVVPB9G1CVZ645WRTB5CGM",
                                "label": "lt",
                                "symbol": "om2:litre"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE8WBHCEJWA61CRSXV3ZZC",
                        "name": "water",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "25",
                            "hasUnit": {
                                "id": "0629XVVPB9G1CVZ645WRTB5CGM",
                                "label": "lt",
                                "symbol": "om2:litre"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "25",
                        "hasUnit": {
                            "id": "0629XVVPB9G1CVZ645WRTB5CGM",
                            "label": "lt",
                            "symbol": "om2:litre"
                        }
                    }
                },
                {
                    "__typename": "EconomicResource",
                    "accountingQuantity": {
                        "hasNumericalValue": "25",
                        "hasUnit": {
                            "id": "0629XVVPB9G1CVZ645WRTB5CGM",
                            "label": "lt",
                            "symbol": "om2:litre"
                        }
                    },
                    "classifiedAs": None,
                    "custodian": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "id": "062AKE8WBHCEJWA61CRSXV3ZZC",
                    "name": "water",
                    "note": None,
                    "onhandQuantity": {
                        "hasNumericalValue": "25",
                        "hasUnit": {
                            "id": "0629XVVPB9G1CVZ645WRTB5CGM",
                            "label": "lt",
                            "symbol": "om2:litre"
                        }
                    },
                    "primaryAccountable": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "raise"
                    },
                    "id": "062AKE8WB5HDJE6HQMM64FFKJ4",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": {
                        "id": "0629XVVR291FGJ0KP6PATHQ9AR",
                        "name": "water",
                        "note": "Specification for water to be used to wash the gowns"
                    },
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "25",
                            "hasUnit": {
                                "id": "0629XVVPB9G1CVZ645WRTB5CGM",
                                "label": "lt",
                                "symbol": "om2:litre"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE8WBHCEJWA61CRSXV3ZZC",
                        "name": "water",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "25",
                            "hasUnit": {
                                "id": "0629XVVPB9G1CVZ645WRTB5CGM",
                                "label": "lt",
                                "symbol": "om2:litre"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "50",
                        "hasUnit": {
                            "id": "0629XVVPB9G1CVZ645WRTB5CGM",
                            "label": "lt",
                            "symbol": "om2:litre"
                        }
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "consume"
                    },
                    "id": "062AKE95TZEMVDK4V2KC83QC1G",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": None,
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "50",
                            "hasUnit": {
                                "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                                "label": "kg",
                                "symbol": "om2:kilogram"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE8VNDSK7Q0858QWWJ9RVM",
                        "name": "soap",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "50",
                            "hasUnit": {
                                "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                                "label": "kg",
                                "symbol": "om2:kilogram"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "50",
                        "hasUnit": {
                            "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                            "label": "kg",
                            "symbol": "om2:kilogram"
                        }
                    }
                },
                {
                    "__typename": "EconomicResource",
                    "accountingQuantity": {
                        "hasNumericalValue": "50",
                        "hasUnit": {
                            "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                            "label": "kg",
                            "symbol": "om2:kilogram"
                        }
                    },
                    "classifiedAs": None,
                    "custodian": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "id": "062AKE8VNDSK7Q0858QWWJ9RVM",
                    "name": "soap",
                    "note": None,
                    "onhandQuantity": {
                        "hasNumericalValue": "50",
                        "hasUnit": {
                            "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                            "label": "kg",
                            "symbol": "om2:kilogram"
                        }
                    },
                    "primaryAccountable": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    }
                },
                {
                    "__typename": "EconomicEvent",
                    "action": {
                        "id": "raise"
                    },
                    "id": "062AKE8VMP4WJF6750DWQKFD1M",
                    "provider": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "receiver": {
                        "id": "0629XVVKAN9W9PA6W6894X7V74",
                        "name": "User Two"
                    },
                    "resourceConformsTo": {
                        "id": "0629XVVQHHNA1JATPVC4GVZB1C",
                        "name": "soap",
                        "note": "Specification for soap to be used to wash the gowns"
                    },
                    "resourceInventoriedAs": {
                        "accountingQuantity": {
                            "hasNumericalValue": "50",
                            "hasUnit": {
                                "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                                "label": "kg",
                                "symbol": "om2:kilogram"
                            }
                        },
                        "classifiedAs": None,
                        "custodian": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        },
                        "id": "062AKE8VNDSK7Q0858QWWJ9RVM",
                        "name": "soap",
                        "note": None,
                        "onhandQuantity": {
                            "hasNumericalValue": "50",
                            "hasUnit": {
                                "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                                "label": "kg",
                                "symbol": "om2:kilogram"
                            }
                        },
                        "primaryAccountable": {
                            "id": "0629XVVKAN9W9PA6W6894X7V74",
                            "name": "User Two"
                        }
                    },
                    "resourceQuantity": {
                        "hasNumericalValue": "100",
                        "hasUnit": {
                            "id": "0629XVVNTQ5QJ0BTSC39N9WCF8",
                            "label": "kg",
                            "symbol": "om2:kilogram"
                        }
                    }
                }
            ]
        }
    }
}
def check_trace(trace_items, events):
    # breakpoint()
    # we reverse the events to have last in first out 
    events.reverse()
    print(f'nr trace: {len(trace_items)}, nr events: {len(events)}')
    print("Check whether there are any duplicated trace items")
    item_ids = {}
    for j, item in enumerate(trace_items):
        if not item['id'] in item_ids:
            item_ids[item['id']] = 1
        else:
            item_ids[item['id']] += 1
            print(f"Item {item['id']} of type {item['__typename']} at pos {j} is a duplicate")

    print("Check whether there are any duplicated events")
    events_ids = {}
    for i, event in enumerate(events):
        if not event['event_id'] in events_ids:
            events_ids[event['event_id']] = 1
        else:
            events_ids[event['event_id']] += 1
            print(f"Event {event['event_id']} with action {event['action']} at pos {i} is a duplicate")

    print("Where are trace items in the events?")
    for j, item in enumerate(trace_items):
        found = False
        for i, event in enumerate(events):
            event_id = event['event_id']
            if item['id'] == event_id:
                print(f"trace item {item['id']} at pos {j} found at pos {i}")
                found = True
        if not found:
            print(f"{item['id']} at pos {j} of type {item['__typename']} not found")

    print("Where are events in the trace?")
    for i, event in enumerate(events):
        found = False
        event_id = event['event_id'] if 'event_id' in event else event['process_id']
        for j,item in enumerate(trace_items):
            if item['id'] == event_id:
                print(f'event pos {i} found at pos {j}')
                found = True
        if not found:
            print(f"{event_id} with action {event['action']} not found")

if __name__ == "__main__":
    trace_items = trace['data']['economicResource']['trace']
    check_trace(trace_items, events)