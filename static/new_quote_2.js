$(function () {
    $('[data-toggle="popover"]').popover()
})

var app = new Vue ({
    el: '#services',
    data: {
        service_list: [],
        price_margin: 80
    },
    computed: {
        total_cost: function () {
            if (!this.service_list) return 0;
            return this.service_list.reduce((acc,current)=>{return acc + current.price;}, 0);
        },
        sell_price: function() {
            return (1 + (this.price_margin/100.0))*this.total_cost;
        },
        s_list: function() {
            return JSON.stringify(this.service_list)
        }
    },
    methods: {
        addService: function(){
            var name = $("#name_value").val();
            var price = parseInt($("#price_value").val());
            if (!name || !price){
                alert("Favor preencher todos os campos");
            }else{
                this.service_list.push({name,price});
                $("#name_value").val('');
                $("#price_value").val('');
            }
        },
        removeService: function(index){
            this.service_list.splice(index,1);
        }
    }
});