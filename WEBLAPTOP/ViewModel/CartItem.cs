using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WEBLAPTOP.ViewModel
{
    public class CartItem
    {
        public int ID_SP { get; set; }
        public string Images_url { get; set; }
        public string TenSP { get; set; }
        public int? GiaBan { get; set; }
        public int? SoLuong { get; set; }
        public decimal? TongTien { get; set; }
    }
}