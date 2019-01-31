function viewModel() {
    var self = this;

    //JQuery
    $resultModal = $('#result-modal');

    $('#file-upload-enabled').change(toggleHandler);
    function toggleHandler() {
        let currentVal = self.hideFileUpload();
        self.hideFileUpload(!currentVal);
    };

    //Form Data
    self.selectedTargetPopulation = ko.observable('all');
    self.selectedRansomType = ko.observable('fixed');
    self.selectedPriceType = ko.observable('no_choice');
    self.ransomValues = ko.observable('');
    self.priceBrackets = ko.observable('');
    self.fixedCosts = ko.observable(0);
    self.example1 = ko.observable(false);
    self.example2 = ko.observable(false);
    self.example3 = ko.observable(false);
    self.example4 = ko.observable(false);
    self.example5 = ko.observable(false);
    self.example6 = ko.observable(false);

    //UI controls/validation
    self.callInProgress = ko.observable(false);
    self.hideFileUpload = ko.observable(false);
    self.noDataSet = ko.observable(true);
    self.imageSrc = ko.observable('');
    self.resultText = ko.observableArray([]);
    
    //Computed functions
	self.disablePopType = ko.computed(function() {
		return self.selectedTargetPopulation() !== 'all' ? true : false;	
	});
	
	self.hidePopType = ko.computed(function() {
		return self.selectedTargetPopulation() == 'all' ? true : false;	
	});
	
	self.hideBrackets = ko.computed(function() {
		return self.selectedPriceType() == 'price_bracket' ? true : false;	
	});
	
    self.enableSave = ko.computed(function() {
        return (self.ransomValues() != null && self.ransomValues() != "") && self.fixedCosts() != null && !self.callInProgress();
    });
    
    self.hidePriceDiscrimination = ko.computed(function(){
        return self.selectedRansomType() !== 'fixed' ? true : false;
    });

    self.imageSource = ko.computed(function(){
        return "data:image/png;base64," + self.imageSrc();       
    });

    self.imageVisible = ko.computed(function(){
        return self.imageSrc().length > 0 ? true : false;                
    });

    self.submitForm = function() {
        self.callInProgress(true);  

        let dataToPost = {
            targetPopulation : self.selectedTargetPopulation(),
            ransomType : self.selectedRansomType(),
            priceDiscriminationType : self.selectedPriceType(),
            ransomValues : self.ransomValues(),
            priceBrackets : self.priceBrackets(),
            fixedCosts: self.fixedCosts(),
            handlingCosts : "",
            example1 : self.example1(),
            example2 : self.example2(),
            example3 : self.example3(),
            example4 : self.example4(),
            example5 : self.example5()
        };

        let formData = new FormData();     
        Object.keys(dataToPost).forEach(function(key) {
            formData.append(key, dataToPost[key]);
        });   
        formData.append('upload-1', $('#upload-1')[0].files[0]);    
        formData.append('upload-2', $('#upload-2')[0].files[0]);
         
        $.ajax({
            type: 'POST',
            url: '/submit_form',
            data: formData,
            contentType: false,
            processData: false,
            success: function(resp) {
                console.log('Post complete.');
                self.callInProgress(false);
                console.log('Post successful.');

                if (resp.success) {
                    self.imageSrc(resp.imageName);
                    self.resultText(resp.myResultsString);
                    self.noDataSet(false);

                    $resultModal.modal('show');
                };            
            },
            error: function() {
                console.log('Post complete.');
                self.callInProgress(false);
                console.log('Post failure.');
            }
        });
    };
};    

ko.applyBindings(new viewModel());